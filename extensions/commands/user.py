import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands
from datetime import datetime
from humanize import naturaldelta

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from tools.ui.paginator import Paginator
from tools.utils import get_avatar_formats

_ = LocalizationStorage("user")

STATUSES = {
    disnake.Status.online: "<:momiji_online_status:1051335123079012372>",
    disnake.Status.dnd: "<:momiji_dnd_status:1051335115206316042> ",
    disnake.Status.idle: "<:momiji_idle_status:1051335120390471701> ",
    disnake.Status.offline: "<:momiji_offline_status:1051335125230686209>"
}


class User(BaseCog):

    @commands.slash_command(name=__("user", key="COMMAND_GROUP_USER"),
                            description=__("user information commands", key="COMMAND_GROUP_DESCRIPTION_USER"))
    async def user(self, inter: AppCmdInter, ):
        ...

    @user.sub_command(name=__("user-info", key="COMMAND_NAME_USER_INFO"),
                      description=__("information and status of the user or member",
                                     key="COMMAND_DESCRIPTION_USER_INFO"))
    async def info_(self, inter: AppCmdInter,
                    user: disnake.User = commands.Param(
                        name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                        description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
                        default=lambda inter: inter.author)):
        locale = _(inter.locale, "profile")
        bool_to_symbol = {True: '+', False: '-'}
        embeds = []
        main_information = [
            f"{locale['full_nikname']} **{user}**",
            f"{locale['created_at']} **<t:{round(user.created_at.timestamp())}:R>** | \
            {(datetime.utcnow() - user.created_at.replace(tzinfo=None)).days} дней "
        ]

        embed = disnake.Embed(
            title=f"{locale['title']} {user.name}"
        ).set_thumbnail(url=user.display_avatar.url).set_footer(text=f"ID: {user.id}")

        if user.banner:
            embed.set_image(url=user.banner.url)

        embeds.append(embed)

        if user in inter.guild.members:
            member = inter.guild.get_member(user.id)
            spotify = list(filter(lambda x: isinstance(x, disnake.activity.Spotify), member.activities))

            embed.title = f"{locale['title']} {user.name} {'📱' if user.is_on_mobile() else '🖥️'}"

            permissions_embed = disnake.Embed(
                title=f'{locale["permissions"]} {member.name}',
                description='```' + 'diff\n' + '\n'.join(
                    [f'{bool_to_symbol[i[-1]]} {i[0].replace("_", " ").capitalize()}' for i in
                     member.guild_permissions]) + '```'
            )

            second_information = [
                f"{locale['joined_at']} **<t:{round(member.joined_at.timestamp())}:R> | {(datetime.utcnow() - member.joined_at.replace(tzinfo=None)).days} {locale['days']}**",
                f"{locale['roles_quantity']} **{len(member.roles) - 1}**\n"
                f"{locale['status']} {STATUSES[member.status]}",
            ]

            embeds.append(permissions_embed)

            if len(spotify):
                data = spotify[0]
                timestamps = (str(data._timestamps['end'])[:10], str(data._timestamps['start'])[:10])

                spotify_embed = disnake.Embed(
                    title=f"{locale['spotify']}",
                    description=f"{locale['song']} [{data.title} | {', '.join(data.artists)}]({data.track_url})\n" 
                                f"{locale['album']} [{data.album}]({data.album_cover_url})\n" 
                                f"{locale['duration']} {naturaldelta(data.duration.total_seconds())} | \
                                <t:{timestamps[0]}:R> - <t:{timestamps[-1]}:R>"
                )
                embeds.append(spotify_embed)

            if len(member.activities) > 0:
                if not member.bot:
                    activities_embed = disnake.Embed(
                        title=f"{locale['activites']} {member}",
                        description='\n'.join(
                            [f'{i.name} | <t:{round(i.created_at.timestamp())}:R>' for i in member.activities])
                    )
                    embeds.append(activities_embed)

        embed.description = "\n".join(main_information) + "\n" + "\n".join(
            second_information) if user in inter.guild.members else "\n".join(main_information)

        if len(embeds) > 1:
            await Paginator(pages=embeds, inter=inter, ephemeral=True).start()
        else:
            await inter.send(embed=embeds[0])

    @user.sub_command(name=__("avatar", key="COMMAND_NAME_AVATAR"),
                      description=__("get member's avatar", key="COMMAND_DESCRIPTION_AVATAR"))
    async def avatar(self, inter: AppCmdInter,
                     member: disnake.Member = commands.Param(
                         default=lambda inter: inter.author,
                         name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                         description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"))
                     ):
        locale = _(inter.locale, "avatar")

        formats = get_avatar_formats(member)
        embed = disnake.Embed(title=f'{locale["title"]} {member.name}',
                              description=' | '.join(formats)
                              ).set_image(url=member.display_avatar.url)

        await inter.send(embed=embed)

    @commands.user_command(name=__("User-information", key="COMMAND_NAME_PROFILE_USER_COMMAND"), )
    async def info(self, inter, member: disnake.Member):
        locale = _(inter.locale, "profile")
        bool_to_symbol = {True: '+', False: '-'}
        embeds = []
        spotify = list(filter(lambda x: isinstance(x, disnake.activity.Spotify), member.activities))
        member_info = [
            f"{locale['status']} {STATUSES[member.status]}",
            f"{locale['full_nikname']} **{member}**",
            f"{locale['created_at']} **<t:{round(member.created_at.timestamp())}:R>**",
            f"{locale['joined_at']} **<t:{round(member.joined_at.timestamp())}:R> | \
            {(datetime.utcnow() - member.joined_at.replace(tzinfo=None)).days} {locale['days']}**",
            f"{locale['roles_quantity']} **{len(member.roles) - 1}**"
        ]

        embed = disnake.Embed(title=f"{locale['title']} {member.name} {'📱' if member.is_on_mobile() else '🖥️'}",
                              description="\n".join(member_info))
        permissions_embed = disnake.Embed(
            title=f'{locale["permissions"]} {member.name}',
            description='```' + 'diff\n' + '\n'.join(
                [f'{bool_to_symbol[i[-1]]} {i[0].replace("_", " ").capitalize()}' for i in
                 member.guild_permissions]) + '```'
        )
        embeds.append(embed)
        embeds.append(permissions_embed)

        if len(spotify):
            data = spotify[0]
            timestamps = (str(data._timestamps['end'])[:10], str(data._timestamps['start'])[:10])

            spotify_embed = disnake.Embed(
                title=f"{locale['spotify']}",
                description=f"{locale['song']} [{data.title} | {', '.join(data.artists)}]({data.track_url})\n" \
                            f"{locale['album']} [{data.album}]({data.album_cover_url})\n" \
                            f"{locale['duration']} {naturaldelta(data.duration.total_seconds())} | \
                            <t:{timestamps[0]}:R> - <t:{timestamps[-1]}:R>"
            )
            embeds.append(spotify_embed)

        if len(member.activities) > 0:
            if not member.bot:
                activities_embed = disnake.Embed(
                    title=f"{locale['activites']} {member}",
                    description='\n'.join(
                        [f'{i.name} | <t:{round(i.created_at.timestamp())}:R>' for i in member.activities])
                )
                embeds.append(activities_embed)

        await Paginator(pages=embeds, inter=inter, ephemeral=True).start()

    @commands.user_command(name=__("Avatar", key="COMMAND_NAME_AVATAR_USER_COMMAND"))
    async def avatar(self, inter, member: disnake.Member):
        locale = _(inter.locale, "avatar")

        formats = get_avatar_formats(member)
        embed = disnake.Embed(title=f'{locale["title"]} {member.name}',
                              description=' | '.join(formats)
                              ).set_image(url=member.display_avatar.url)

        await inter.send(embed=embed)


def setup(client: commands.InteractionBot):
    client.add_cog(User(client))
