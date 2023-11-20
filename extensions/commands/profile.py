import disnake
from disnake import AppCmdInter, UserCommandInteraction
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage

from tools.utils import profile
from tools.exeption import CustomError

_ = LocalizationStorage("profile")
err = LocalizationStorage('errors#2')


class Profile(BaseCog):

    @commands.slash_command(name=__("profile", key="COMMAND_GROUP_PROFILE"),
                            description=__("profile commands", key="COMMAND_GROUP_DESCRIPTION_PROFILE"))
    async def profile(self, inter: AppCmdInter):
        ...

    @profile.sub_command(name=__("create", key="COMMAND_NAME_PROFILE_CREATE"),
                         description=__("create a profile on the server", key="COMMAND_DESCRIPTION_PROFILE_CREATE"))
    async def create(self, inter: AppCmdInter):
        locale = _(inter.locale, "profile_create")
        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.author.guild.id)
        author_user_in_db = await self.client.db.Users.get_or_create(discord_id=inter.author.id)
        author_profile = await self.client.db.Profiles.get_or_create(user=author_user_in_db[0], server=server_in_db[0])
        if author_profile[1]:
            return await inter.send(
                embed=disnake.Embed(
                    title=locale['title'],
                    description=locale['description']
                )
            )
        await inter.send(
            embed=disnake.Embed(
                title=locale["error"]
            )
        )

    @profile.sub_command(name=__("view", key="COMMAND_NAME_VIEW"),
                         description=__("view profile", key="COMMAND_DESCRIPTION_VIEW"))
    async def view(self, inter: AppCmdInter,
                   member: disnake.Member = commands.Param(
                       name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                       description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
                       default=lambda inter: inter.author)
                   ):
        locale = _(inter.locale, "profile_view")
        loc = err(inter.locale, "errors")
        if member.bot:
            raise CustomError(loc['bot_error'])
        await profile(locale, self.client, inter, member)

    @commands.user_command(name=__("Profile", key="COMMAND_NAME_PROFILE"))
    async def _view(self, inter: UserCommandInteraction, member: disnake.Member):
        locale = _(inter.locale, "profile_view")
        loc = err(inter.locale, "errors")
        if member.bot:
            raise CustomError(loc['bot_error'])
        await profile(locale, self.client, inter, member)


def setup(client: commands.InteractionBot):
    client.add_cog(Profile(client))
