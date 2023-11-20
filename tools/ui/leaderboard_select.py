import disnake
from disnake.ext import commands
from .components import StandardSelect
from tools.utils import divide_chunks
from tools.ui.paginator import Paginator


async def send_top(inter: disnake.MessageInteraction, client: commands.InteractionBot, locale: dict, top_type, server,
                   select):
    sorted_profiles = await client.db.Profiles.filter(server=server).order_by(f'-{top_type}').limit(
        50).prefetch_related("user")
    other_pages_profiles = list(divide_chunks(sorted_profiles[10:], 10))

    first_page = disnake.Embed(
        description='',
        title=locale[f'title_select_{top_type}']
    )

    if top_type == "money":
        emoji = client.emojies.money_emoji
    elif top_type == "level":
        emoji = client.emojies.level_emoji
    else:
        emoji = client.emojies.messages_emoji

    for i, profiles in enumerate(sorted_profiles[:10], start=1):
        user_in_discord: disnake.Member = inter.guild.get_member(profiles.user.discord_id)
        if top_type == "money":
            top = profiles.money
        elif top_type == "level":
            top = profiles.level
        else:
            top = profiles.messages
        user_description = profiles.description
        if user_description is None:
            user_description = locale["description_none"]
        first_page.description += f"**{i})** {user_in_discord.mention} - {top} {emoji}\n{locale['profile_description']}\
                                  - {user_description}\n"
    pages = [first_page]

    start = 1

    for ten_leaderboard in other_pages_profiles:
        temp_page = disnake.Embed(
            description='',
            title=locale[f'title_select_{top_type}']
        )
        start += 10
        for i, other_profiles in enumerate(ten_leaderboard, start=start):
            user_in_discord: disnake.Member = inter.guild.get_member(other_profiles.user.discord_id)
            if top_type == "money":
                top = other_profiles.money
            elif top_type == "level":
                top = other_profiles.level
            else:
                top = other_profiles.messages
            user_description = other_profiles.description
            if user_description is None:
                user_description = locale["description_none"]
            temp_page.description += f"**{i})** {user_in_discord.mention} \
             - {top} {emoji}\n{locale['profile_description']} - {user_description}\n"
        pages.append(temp_page)

    if len(pages) < 2:
        return await inter.response.edit_message(embed=pages[0])

    await Paginator(pages=pages, inter_resp=inter, timeout=60, ephemeral=True, childrens=[select]).start_edit_resp()


class LeaderBoardSelect(StandardSelect):

    def __init__(self, locale, server, client):
        self.locale = locale
        self.server = server
        self.client = client
        components = [
            disnake.SelectOption(label=self.locale["top_balance"], emoji="<a:momiji_crystal:1126456975337730078>"),
            disnake.SelectOption(label=self.locale["top_message"], emoji="<:momiji_message:1127503836429438976>"),
            disnake.SelectOption(label=self.locale["top_level"], emoji="<:momiji_activity:1127504341482344489>"),
        ]
        super().__init__(options=components, placeholder=locale['placeholder'])

    async def callback(self, interaction: disnake.MessageInteraction):
        if self.values[0] == self.locale["top_balance"]:
            await send_top(interaction, self.client, self.locale, "money", self.server, self)
        elif self.values[0] == self.locale["top_message"]:
            await send_top(interaction, self.client, self.locale, "messages", self.server, self)
        else:
            await send_top(interaction, self.client, self.locale, "level", self.server, self)
