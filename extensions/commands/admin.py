import disnake
from disnake.ext import commands
from disnake import Localized as __

from core.checks import BaseChecks
from core.cog import BaseCog
from core.i18n import LocalizationStorage
from core.models.profiles import Profiles
from core.models.servers import Servers
from tools.ui.components import StandartView
from tools.utils import get_or_create_profile
from tools.ui.admin_panel.buttons import RatingPanelButtons, StubButton, BanButton, KickButton

_ = LocalizationStorage("administration")
err = LocalizationStorage("errors#2")

RATING_TYPES = ["level", "money", "messages", "experience"]
EMOJIS_RATING = ["<:momiji_activity:1127504341482344489>",
                 "<a:momiji_crystal:1126456975337730078>",
                 "<:momiji_message:1127503836429438976>",
                 "<a:momiji_experience:1126492132086136892>"]


class Administration(BaseCog):

    @commands.slash_command()
    async def administration(self, inter: disnake.AppCmdInter):
        ...

    # @commands.has_permissions(administration=True)
    @BaseChecks.is_higher(err)
    @BaseChecks.bot_check(err)
    @administration.sub_command()
    async def panel(self, inter: disnake.AppCmdInter,
                    member: disnake.Member = commands.Param(
                        name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                        description=__("member for moderate", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
                        default=lambda inter: inter.author)):
        locale = _(inter.locale, "panel")
        server: tuple[Servers, bool] = await self.client.db.Servers.get_or_create(discord_id=member.guild.id)
        # moderator: Profiles = await get_or_create_profile(self.client, server, inter.author, ["user"])
        member_in_db: Profiles = await get_or_create_profile(self.client, server, member, ["user", "tickets", "warns"])
        embed = disnake.Embed(description=locale["description"].format(member=member.mention, money=member_in_db.money,
                                                                       level=member_in_db.level,
                                                                       messages=member_in_db.messages,
                                                                       experience=member_in_db.experience,
                                                                       warns=len(await member_in_db.warns),
                                                                       tickets=len(await member_in_db.tickets)))\
            .set_thumbnail(url=member.display_avatar)\
            .set_author(icon_url=inter.guild.icon,
                        name=f"{locale['author_name']}{member.display_name}")
        view = StandartView(inter, self.client, timeout=30)
        if member != inter.author:
            view.add_item(StubButton(row=1, emoji="⚒️", style=disnake.ButtonStyle.grey, label="label_mod", locale=locale,
                                     type_="mod_about"))
            view.add_item(BanButton(member=member, locale=locale, embed=embed))
            view.add_item(KickButton(member=member, locale=locale, embed=embed))
        view.add_item(StubButton(row=2, emoji="🔝", style=disnake.ButtonStyle.grey, label="label_rate", locale=locale,
                                 type_="rate_about"))
        for i in range(4):
            view.add_item(RatingPanelButtons(EMOJIS_RATING[i], RATING_TYPES[i], member, member_in_db, embed, locale))
        await inter.send(embed=embed, view=view)


def setup(client: commands.InteractionBot):
    client.add_cog(Administration(client))
