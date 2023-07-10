import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from core.checks import BaseChecks
from tools.exeption import CustomError
from tools.utils import get_member_profile
from tools.utils import divide_chunks
from tools.ui.paginator import Paginator
from tortoise.exceptions import DoesNotExist

_ = LocalizationStorage("moderation")
err = LocalizationStorage("errors#2")


class Moderation(BaseCog):

    @commands.slash_command(name=__("moderation", key="COMMAND_GROUP_MODERATION"),
                            description=__("moderation commands", key="COMMAND_GROUP_DESCRIPTION_MODERATION"))
    async def moderation(self, inter: AppCmdInter):
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
        # duration: int = commands.Param(name="do_not_work", default=None),
        # unit=commands.Param(
        #     name="do_not_work_too",
        #     choices=[
        #         __("seconds", key="SECONDS"),
        #         __("minutes", key="MINUTES"),
        #         __("hours", key="HOURS"),
        #         __("days", key="DAYS"),
        #         __("weeks", key="WEEKS")
        #     ],
        #     default=None
        # )
    ):
        locale = _(inter.locale, "ban")
        reason_ = locale['not_reason'] if not reason else reason

        await inter.guild.ban(user=member, reason=reason_)

        await inter.send(
            embed=disnake.Embed(
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
                embed=disnake.Embed(
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
            embed=disnake.Embed(
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
        unit=commands.Param(
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
            embed=disnake.Embed(
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
            embed=disnake.Embed(
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

    @BaseChecks.is_higher(err)
    @BaseChecks.self_check(err)
    @BaseChecks.bot_check(err)
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @moderation.sub_command(
        name=__("warn", key="COMMAND_NAME_WARN"),
        description=__("warn server's member", key="COMMAND_DESCRIPTION_WARN")
    )
    async def warn(
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
        locale = _(inter.locale, "warn")
        profile_in_db = await get_member_profile(member, self.client, "server") 
        moder_profile = await get_member_profile(inter.author, self.client)
        server_warns = await self.client.db.Warns.filter(server=profile_in_db.server.id).order_by("-number").limit(1)
        if len(server_warns) < 1:
            number = 1
        else:
            number = server_warns[0].number+1
        await self.client.db.Warns.create(number=number, server=profile_in_db.server, profile=profile_in_db, reason=reason, moderator=moder_profile)
        if reason is None:
            reason = locale["not_reason"]
        await inter.send(
            embed=disnake.Embed(
                title=locale['title'], description=locale['description'],
                color=disnake.Color.red()
            ).add_field(
                name=locale["field_name_1"], value=member.mention
            ).add_field(
                name=locale["field_name_2"], value=reason
            ).add_field(
                name=locale["field_name_3"], value=member.id, inline=False
            ).set_thumbnail(
                url=member.display_avatar.url
            ).set_footer(
                text=f'{locale["footer_text"]}: {number}', icon_url=inter.author.display_avatar.url
            )
        )

    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @moderation.sub_command(
        name=__("unwarn", key="COMMAND_NAME_UNWARN"),
        description=__("unwarn server's member", key="COMMAND_DESCRIPTION_UNWARN")
    )
    async def unwarn(
        self, inter: AppCmdInter,
        case: int = commands.Param(
            name=__("case-number", key="COMMAND_PARAM_NAME_CASE"),
            description=__("enter case number", key="COMMAND_PARAM_DESCRIPTION_CASE")
        )
    ):
        locale = _(inter.locale, "unwarn")
        server = await self.client.db.Servers.get(discord_id=inter.guild.id)
        try:
            warn  = await self.client.db.Warns.filter(server=server.id, number=case).limit(1).prefetch_related("profile", "profile__user", "moderator", "moderator__user")

            if inter.author.id == warn[0].profile.user.discord_id:
                raise CustomError(locale["self_error"])

            user_in_discord: disnake.Member = inter.guild.get_member(warn[0].profile.user.discord_id)
            moderator_in_discord: disnake.Member = inter.guild.get_member(warn[0].moderator.user.discord_id)
            if warn[0].reason is None:
                reason = locale["not_reason"]
            else:
                reason = warn[0].reason

            await inter.send(
                embed = disnake.Embed(
                    title=locale['title'],
                    description=locale['description'],
                    color=disnake.Color.green()
                ).add_field(
                    name=locale['field_name_1'],
                    value=user_in_discord.mention
                ).add_field(
                    name=locale['field_name_2'],
                    value=moderator_in_discord.mention
                ).add_field(
                    name=locale['field_name_3'],
                    value=reason
                )
            )

            await warn[0].delete()
        except IndexError:
            raise CustomError(locale["not_warn"])

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
            le=100
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
            embed=disnake.Embed(
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

    @moderation.sub_command(
        name=__("server-warns", key="COMMAND_NAME_SWARNS"),
        description=__("display all server's warns", key="COMMAND_DESCRIPTION_SWARNS")
    )
    async def server_warns(self, inter: AppCmdInter):
        locale = _(inter.locale, "server_warns")
        server_in_db = await self.client.db.Servers.get(discord_id=inter.guild.id)
        warns = await self.client.db.Warns.filter(server=server_in_db.id).order_by("number").prefetch_related("profile", "profile__user", "moderator", "moderator__user")
        other_pages = list(divide_chunks(warns[5:], 5))

        if len(warns) < 1:
            raise CustomError(locale["not_warns"])

        first_page = disnake.Embed(
            description=locale['description'],
            title=locale[f'title']
        )

        for warns in warns[:5]:
            if warns.reason is None:
                reason = locale["not_reason"]
            else:
                reason = warns.reason
            user_in_discord: disnake.Member = inter.guild.get_member(warns.profile.user.discord_id)
            moderator_in_discord: disnake.Member = inter.guild.get_member(warns.moderator.user.discord_id)
            first_page.add_field(name=warns.number,
                value=f"{user_in_discord.mention}\n**{locale['reason']}** - {reason}\n"\
                      f"**{locale['moderator']}** - {moderator_in_discord.mention}", 
                inline=False)
        
        pages = [first_page]

        start = 1

        for ten_warns in other_pages:
            temp_page = disnake.Embed(
                description=locale['description'],
                title=locale[f'title']
            )
            start += 5
            for warns in ten_warns:
                if warns.reason is None:
                    reason = locale["not_reason"]
                else:
                    reason = warns.reason
                user_in_discord: disnake.Member = inter.guild.get_member(warns.profile.user.discord_id)
                moderator_in_discord: disnake.Member = inter.guild.get_member(warns.moderator.user.discord_id)
                temp_page.add_field(
                    name=warns.number, 
                    value=f"{user_in_discord.mention}\n**{locale['reason']}** - {reason}\n"\
                          f"**{locale['moderator']}** - {moderator_in_discord.mention}",
                    inline=False)
            pages.append(temp_page)

        if len(pages) < 2:
            return await inter.send(inter.author.mention, embed=pages[0])
        
        await Paginator(pages=pages, inter=inter, timeout=60).start(inter.author.mention)

    @moderation.sub_command(
        name=__("user-warns", key="COMMAND_NAME_UWARNS"),
        description=__("display all user's warns", key="COMMAND_DESCRIPTION_UWARNS")
    )
    async def user_warns(
        self, inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            default=lambda inter: inter.author,
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("member for moderate", key="COMMAND_PARAM_DESCRIPTION_MEMBER")
        )
    ):
        locale = _(inter.locale, "user_warns")
        profile_in_db = await get_member_profile(member, self.client)
        warns = await self.client.db.Warns.filter(profile=profile_in_db).order_by("number").prefetch_related("moderator", "moderator__user")
        other_pages = list(divide_chunks(warns[5:], 5))

        if len(warns) < 1:
            raise CustomError(locale["not_warns"])

        first_page = disnake.Embed(
            description=locale['description'],
            title=locale[f'title']
        )

        for i, warns in enumerate(warns[:5], start=1):
            if warns.reason is None:
                reason = locale["not_reason"]
            else:
                reason = warns.reason
            moderator_in_discord: disnake.Member = inter.guild.get_member(warns.moderator.user.discord_id)
            first_page.add_field(name=i,
                value=f"{locale['number']} - {warns.number}\n"\
                      f"**{locale['reason']}** - {reason}\n"\
                      f"**{locale['moderator']}** - {moderator_in_discord.mention}", 
                inline=False)
        
        pages = [first_page]

        start = 1

        for ten_warns in other_pages:
            temp_page = disnake.Embed(
                description=locale['description'],
                title=locale[f'title']
            )
            start += 5
            for i, warns in enumerate(ten_warns, start=start):
                if warns.reason is None:
                    reason = locale["not_reason"]
                else:
                    reason = warns.reason
                moderator_in_discord: disnake.Member = inter.guild.get_member(warns.moderator.user.discord_id)
                temp_page.add_field(name=i,
                    value=f"{locale['number']} - {warns.number}\n"\
                        f"**{locale['reason']}** - {reason}\n"\
                        f"**{locale['moderator']}** - {moderator_in_discord.mention}", 
                    inline=False)
            pages.append(temp_page)
        
        if len(pages) < 2:
            return await inter.send(inter.author.mention, embed=pages[0])
        
        await Paginator(pages=pages, inter=inter, timeout=60).start(inter.author.mention)


def setup(client: commands.InteractionBot):
    client.add_cog(Moderation(client))
