import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from tools.utils import split_guild_members

_ = LocalizationStorage("info")


class Info(BaseCog):

    @commands.slash_command(
        name=__("info", key="COMMAND_GROUP_INFO"),
        description=__("info commands", key="COMMAND_GROUP_DESCRIPTION_INFO")
    )
    async def info(self, inter: AppCmdInter):
        ...

    @info.sub_command(
        name=__('help', key="COMMAND_NAME_HELP"),
        description=__('help command', key="COMMAND_DESCRIPTION_HELP")
    )
    async def help(self, inter: AppCmdInter):
        locale = _(inter.locale, "help")
        await inter.send(
            embed=disnake.Embed(
                title=locale['title'],
                description=locale['description']
            ).set_footer(
                text=locale['footer']
            ).set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1123682099233300602/1123682190627180554/40fa8a79c6d4c2e5add6ae6b97fc261c.jpg"
            )
        )

    @info.sub_command(
        name=__('bot-info', key="COMMAND_NAME_BOT-INFO"),
        description=__('information and status of the bot', key="COMMAND_DESCRIPTION_BOT-INFO")
    )
    async def _bot_info(self, inter: AppCmdInter):
        locale = _(inter.locale, "bot_info")
        BOT_INFO = [
            "<@799139246928560139>", 
            "<t:1651903200:f>", "3.10", 
            "**[Disnake 2.9.0](https://docs.disnake.dev/en/stable/)**", 
            f"{len(self.client.guilds)}", f"{self.client.latency * 1000:.0f} ms"
        ]

        embed = disnake.Embed(
            title=locale['title'],
            description=locale['description']
        )

        for count in range(len(BOT_INFO)):
            embed.add_field(
                name=locale[f'field_name_{count}'],
                value=BOT_INFO[count]
            )

        await inter.send(embed=embed)

    @info.sub_command(
        name=__('server', key="COMMAND_NAME_SERVER"),
        description=__('server info', key="COMMAND_DESCRIPRION_SERVER")
    )
    async def server(self, inter: AppCmdInter):
        locale = _(inter.locale, "server")
        guild = inter.guild

        descr = guild.description
        bots, members = split_guild_members(guild.members)

        embed = disnake.Embed(
            title=f"{locale['title']} {guild.name}",
            description=descr if descr else locale['description']
        ).add_field(
            name=f"{locale['field_name_1']}",
            value=f"{locale['field_value_1']} {len(members)}\n"
                  f"{locale['field_value_2']} {len(bots)}\n"
                  f"{locale['field_value_3']} {len(bots) + len(members)}"
        ).add_field(
            name=locale['field_name_2'],
            value=f"<:momiji_online_status:1051335123079012372>: **{len(list(filter(lambda x: x.status == disnake.Status.online, guild.members)))}**\n"
                  f"<:momiji_dnd_status:1051335115206316042>: **{len(list(filter(lambda x: x.status == disnake.Status.dnd, guild.members)))}**\n"
                  f"<:momiji_idle_status:1051335120390471701>: **{len(list(filter(lambda x: x.status == disnake.Status.idle, guild.members)))}**\n"
                  f"<:momiji_offline_status:1051335125230686209>: **{len(list(filter(lambda x: x.status == disnake.Status.offline, guild.members)))}**" 
        ).add_field(
            name=locale['field_name_3'],
            value=f'{locale["field_value_4"]} **{len(guild.channels)}**\n'
                  f'{locale["field_value_5"]} **{len(guild.voice_channels)}**\n'
                  f'{locale["field_value_6"]} **{len(guild.text_channels)}**\n'
                  f'{locale["field_value_7"]} **{len(guild.threads)}**\n'
                  f'{locale["field_value_8"]} {guild.rules_channel.mention if guild.rules_channel else locale["null"]}\n'
                  f'{locale["field_value_9"]} {guild.system_channel.mention if guild.system_channel else locale["null"]}'
        ).add_field(
            name=locale['field_name_4'],
            value=f'{locale["field_value_10"]} **{locale["yes"] if guild.premium_progress_bar_enabled else locale["no"]}**\n'
                  f'{locale["field_value_11"]} **{len(guild.premium_subscribers)}**\n'
                  f'{locale["field_value_12"]} **{guild.premium_tier}**'
        ).add_field(
            name=locale['field_name_5'],
            value=f'{locale["field_value_13"]} **{len(guild.stickers)}**\n'
                  f'{locale["field_value_14"]} **{len(guild.emojis)}**\n'
                  f'{locale["field_value_16"]} <@{guild.owner.id}>\n'
                  f'{locale["field_value_17"]} **{guild.max_members}**\n'
                  f'{locale["field_value_18"]} **{guild.shard_id}**\n'
                  f'{locale["field_value_19"]} <t:{round(guild.created_at.timestamp())}:R>\n'
                  f'{locale["field_value_15"]} {locale["null"]}' if not guild.splash else f'{locale["field_value_15"]}: [{locale["link"]}]({guild.splash})'
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        if guild.banner:
            embed.set_image(url=guild.banner.url)

        await inter.send(embed=embed)

def setup(client: commands.InteractionBot):
    client.add_cog(Info(client))