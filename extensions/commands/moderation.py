import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from core.checks import BaseChecks
from tools.exeption import CustomError

_ = LocalizationStorage("moderation")
err = LocalizationStorage("errors#2")

class Moderation(BaseCog):

    @commands.slash_command(
        name=__("moderation", key="COMMAND_GROUP_MODERATION")
    )
    async def moderation(self, inter:AppCmdInter):
        ...

    @BaseChecks.is_higher(err)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @moderation.sub_command(
        name=__("ban", key="COMMAND_NAME_BAN"),
        description=__("ban member on server", key="COMMAND_DESCRIPTION_BAN")
    )
    async def ban(
        self, 
        inter: AppCmdInter,
        member: disnake.User = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("member for ban", key="COMMAND_PARAM_DESCRIPTION_MEMBER")
        ),
        reason: str = commands.Param(
            name=__("reason", key="COMMAND_PARAM_NAME_REASON"),
            description=__("reason for ban", key="COMMAND_PARAM_DESCRIPTION_REASON"),
            default=None
        ),
        duration: int = commands.Param(name="do_not_work", default=None),
        unit = commands.Param(
            name="do_not_work_too",
            choices=[
                __("seconds", key="SECONDS"),
                __("minutes", key="MINUTES"),
                __("hours", key="HOURS"),
                __("days", key="DAYS"),
                __("weeks", key="WEEKS")
            ],
            default=None
        )
    ):
        locale = _(inter.locale, "ban")
        reason_ = locale['not_reason'] if not reason else reason
        
        await inter.guild.ban(user=member, reason=reason_)
        
        await inter.send(
            embed = disnake.Embed(
                title=locale['title'],
                description=locale['description'],
                colour=disnake.Colour.red()
            ).add_field(
                name=locale["field_name_1"],
                value=member.mention,
                inline=False
            ).add_field(
                name=locale["field_name_2"],
                value=reason_
            ).add_field(
                name=locale["field_name_3"],
                value=member.id
            ).set_thumbnail(
                url=member.display_avatar.url
            )
        )
    
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @moderation.sub_command(
        name=__("unban", key="COMMAND_NAME_UNBAN"),
        description=__("unban user on server", key="COMMAND_DESCRIPTION_UNBAN")
    )
    async def unban(
        self, 
        inter: AppCmdInter, 
        member_id: int = commands.Param(
            name=__("id", key="COMMAND_PARAM_NAME_ID"),
            description=__("user id", key="COMMAND_PARAM_DESCRIPTION_ID"),
            large=True
        ),
        reason: str = commands.Param(
            name=__("reason", key="COMMAND_PARAM_NAME_REASON"),
            description=__("reason for moderate", key="COMMAND_PARAM_DESCRIPTION_REASON"),
            default=None
        )
    ):
        locale = _(inter.locale, "unban")
        user = await self.client.fetch_user(member_id)
        reason_ = locale['not_reason'] if not reason else reason
        try:
            await inter.guild.unban(user=user, reason=reason_)
            await inter.send(
                embed = disnake.Embed(
                    title=locale['title'],
                    description=locale['description'],
                    color=disnake.Colour.green()
                ).add_field(
                    name=locale['field_name_1'],
                    value=user.mention,
                    inline=False
                ).add_field(
                    name=locale['field_name_2'],
                    value=reason_
                ).add_field(
                    name=locale['field_name_3'],
                    value=user.id
                ).set_thumbnail(
                    url=user.display_avatar.url
                )
            )
        except:
            raise CustomError(locale['error'])

    @BaseChecks.is_higher(err)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @moderation.sub_command(
        name=__("kick", key="COMMAND_NAME_KICK"),
        description=__("kick member from the server", key="COMMAND_DESCRIPTION_KICK")
    )
    async def kick(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("member for moderate", key="COMMAND_PARAM_DESCRIPTION_MEMBER")
        ),
        reason: str = commands.Param(
            name=__("reason", key="COMMAND_PARAM_NAME_REASON"),
            description=__("reason for moderate", key="COMMAND_PARAM_DESCRIPTION_REASON"),
            default=None
        )
    ):
        locale = _(inter.locale, "kick")
        reason_ = locale['not_reason'] if not reason else reason

        await inter.guild.kick(user=member, reason=reason_)
        
        await inter.send(
            embed = disnake.Embed(
                title=locale['title'],
                description=locale['description'],
                colour=disnake.Colour.red()
            ).add_field(
                name=locale["field_name_1"],
                value=member.mention,
                inline=False
            ).add_field(
                name=locale["field_name_2"],
                value=reason_
            ).add_field(
                name=locale["field_name_3"],
                value=member.id
            ).set_thumbnail(
                url=member.display_avatar.url
            )
        )

    @BaseChecks.is_higher(err)
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @moderation.sub_command(
        name=__("mute", key="COMMAND_NAME_MUTE"),
        description=__("mute server's member", key="COMMAND_DESCRIPTION_MUTE")
    )
    async def mute(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("member for moderate", key="COMMAND_PARAM_DESCRIPTION_MEMBER")
        ),
        duration: int = commands.Param(
            name=__("duration", key="COMMAND_PARAM_NAME_DURATION"),
            description=__("select duration", key="COMMAND_PARAM_DESCRIPTION_DURATION")
        ),
        unit = commands.Param(
            name=__("unit", key="COMMAND_PARAM_NAME_UNIT"),
            description=__("select unit", key="COMMAND_PARAM_DESCRIPTION_UNIT"),
            choices=[
                __("seconds", key="SECONDS"),
                __("minutes", key="MINUTES"),
                __("hours", key="HOURS"),
                __("days", key="DAYS"),
                __("weeks", key="WEEKS")
            ]
        ),
        reason: str = commands.Param(
            name=__("reason", key="COMMAND_PARAM_NAME_REASON"),
            description=__("reason for moderate", key="COMMAND_PARAM_DESCRIPTION_REASON"),
            default=None
        )
    ):
        locale = _(inter.locale, "mute")
        reason_ = locale['not_reason'] if not reason else reason
        units = {
            "seconds" or "секунд": duration,
            "minutes" or "минут": duration * 60,
            "hours" or "часов": duration * 3600,
            "days" or "дней": duration * 86400,
            "weeks" or "недель": duration * 604800
        }

        await inter.guild.timeout(user=member, duration=units[unit], reason=reason_)

        await inter.send(
            embed = disnake.Embed(
                title=locale['title'],
                description=locale['description'],
                colour=disnake.Colour.red()
            ).add_field(
                name=locale["field_name_1"],
                value=member.mention
            ).add_field(
                name=locale["field_name_2"],
                value=f"{duration} {unit}"
            ).add_field(
                name=locale["field_name_3"],
                value=reason_,
                inline=False
            ).add_field(
                name=locale["field_name_4"],
                value=member.id
            ).set_thumbnail(
                url=member.display_avatar.url
            )
        )

    @BaseChecks.is_higher(err)
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @moderation.sub_command(
        name=__("unmute", key="COMMAND_NAME_UNMUTE"),
        description=__("unmute server's member", key="COMMAND_DESCRIPTION_UNMUTE")
    )
    async def unmute(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("member for moderate", key="COMMAND_PARAM_DESCRIPTION_MEMBER")
        ),
        reason: str = commands.Param(
            name=__("reason", key="COMMAND_PARAM_NAME_REASON"),
            description=__("reason for moderate", key="COMMAND_PARAM_DESCRIPTION_REASON"),
            default=None
        )
    ):
        locale = _(inter.locale, "unmute")
        reason_ = locale['not_reason'] if not reason else reason
        await inter.guild.timeout(user=member, duration=0, reason=reason_)
        await inter.send(
            embed = disnake.Embed(
                title=locale['title'],
                description=locale['description'],
                color=disnake.Colour.green()
            ).add_field(
                name=locale['field_name_1'],
                value=member.mention,
                inline=False
            ).add_field(
                name=locale['field_name_2'],
                value=reason_
            ).add_field(
                name=locale['field_name_3'],
                value=member.id
            ).set_thumbnail(
                url=member.display_avatar.url
            )
        )

    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @moderation.sub_command(
        name=__('clear', key='COMMAND_NAME_CLEAR'),
        description=__('clear messages in channel', key='COMMAND_DESCRIPTION_CLEAR')
    )
    async def clear(
        self,
        inter: AppCmdInter,
        count: int = commands.Param(
            name=__("count", key="COMMAND_PARAM_NAME_COUNT"),
            description=__("count messages", key="COMMAND_PARAM_DESCRIPTION_COUNT"),
            ge=1,
            le= 100
        ),
        channel: disnake.TextChannel = commands.Param(
            name=__("channel", key="COMMAND_PARAM_NAME_CHANNEL"),
            description=__("select channel", key="COMMAND_PARAM_DESCRIPTION_CHANNEL"),
            default=None
        )
    ):
        locale = _(inter.locale, "clear")
        channel_ = inter.channel if not channel else channel
        messages = await inter.channel.purge(limit=count) if not channel else await channel.purge(limit=count)

        await inter.send(
            embed = disnake.Embed(
                title=locale['title'],
                description=locale['description'],
                color=disnake.Colour.green()
            ).add_field(
                name=locale['field_name_1'],
                value=channel_.mention,
                inline=False
            ).add_field(
                name=locale['field_name_2'],
                value=len(messages)
            )
        )

def setup(client: commands.InteractionBot):
    client.add_cog(Moderation(client))