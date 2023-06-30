import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

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



        member_info = [
            f"{locale['status']} {STATUSES[member.status]}",
            f"{locale['full_nikname']} **{str(member)}**",
            f"{locale['created_at']} **<t:{round(member.created_at.timestamp())}:R>**",
            f"{locale['roles_quantity']} **{len(member.roles)-1}**"
        ]

        if member.joined_at:
            member_info.insert(3, f"{locale['joined_at']}: **<t:{round(member.joined_at.timestamp())}:R>**")

        embed = disnake.Embed(title=f"{locale['title']} **{member.display_name}**",
                                description="\n".join(member_info)
        ).set_thumbnail(url=member.display_avatar.url).set_footer(text=f"ID: {member.id}")

        if member.banner:
            embed.set_image(url=member.banner.url)
            view = None

        await inter.send(embed=embed)

def setup(client: commands.InteractionBot):
    client.add_cog(User(client))