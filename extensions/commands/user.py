import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands
import datetime
from humanize import naturaldelta

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from tools.ui.paginator import Paginator

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
    async def user(self, inter: AppCmdInter):
        ...

    # @user.sub_command(name=__("user-info", key="COMMAND_NAME_USER-INFO"),
    #                   description=__("information and status of the user", key="COMMAND_DESCRIPTION_USER-INFO"))
    # async def info_():
    #     ...

    @commands.user_command(name=__("profile", key="COMMAND_NAME_PROFILE_USER-COMMAND"),)
    async def info(self, inter, member: disnake.Member):
        locale = _(inter.locale, "profile")
        bool_to_symbol = {True: '+', False: '-'}
        embeds = []
        spotify = list(filter(lambda x: isinstance(x, disnake.activity.Spotify), member.activities))
        member_info = [
            f"{locale['status']} {STATUSES[member.status]}",
            f"{locale['full_nikname']} **{str(member)}**",
            f"{locale['created_at']} **<t:{round(member.created_at.timestamp())}:R>**",
            f"{locale['joined_at']} **<t:{round(member.joined_at.timestamp())}:R> | {(datetime.datetime.utcnow() - member.joined_at.replace(tzinfo=None)).days} {locale['days']}**",
            f"{locale['roles_quantity']} **{len(member.roles)-1}**"
        ]

        embed = disnake.Embed(title=f"{locale['title']} {member.name} {'📱' if member.is_on_mobile() else '🖥️'}",
                              description="\n".join(member_info))
        permissions_embed = disnake.Embed(
            title=f'{locale["permissions"]} {member.name}',
            description='```' + 'diff\n' + '\n'.join([f'{bool_to_symbol[i[-1]]} {i[0].replace("_", " ").capitalize()}' for i in member.guild_permissions]) + '```'
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
                                f"{locale['duration']} {naturaldelta(data.duration.total_seconds())} | <t:{timestamps[0]}:R> - <t:{timestamps[-1]}:R>"
                )
                embeds.append(spotify_embed)
        
        if len(member.activities) > 0:
            if not member.bot:
                activities_embed = disnake.Embed(
                    title=f"{locale['activites']} {member}",
                    description='\n'.join([f'{i.name} | <t:{round(i.created_at.timestamp())}:R>' for i in member.activities])
                )
                embeds.append(activities_embed)
        
        await Paginator(pages=embeds, inter=inter, ephemeral=True).start()

def setup(client: commands.InteractionBot):
    client.add_cog(User(client))