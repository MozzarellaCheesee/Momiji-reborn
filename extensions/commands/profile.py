import disnake
from disnake import AppCmdInter, UserCommandInteraction
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage

from tools.utils import profile

_ = LocalizationStorage("profile")

class Profile(BaseCog):
    
    @commands.slash_command()
    async def profile(self, inter: AppCmdInter):
        ...

    @profile.sub_command()
    async def view(self, inter: AppCmdInter,
                   member: disnake.Member = commands.Param(
                        name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                        description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
                        default=lambda inter: inter.author)
    ):
        locale = _(inter.locale, "profile_view")
        await profile(locale, self.client, inter, member)

    @commands.user_command()
    async def _view(self, inter: UserCommandInteraction, member: disnake.Member):
        locale = _(inter.locale, "profile_view")
        await profile(locale, self.client, inter, member)

    
    
def setup(client: commands.InteractionBot):
    client.add_cog(Profile(client))