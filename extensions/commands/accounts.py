import disnake
from disnake import AppCmdInter, UserCommandInteraction
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from tools.utils import account as acc


_ = LocalizationStorage("user")

class Accounts(BaseCog):
    
    @commands.slash_command(name=__("account", key="COMMAND_NAME_ACCOUNT"),
                      description=__("User account in the bot system", key="COMMAND_DESCRIPTION_ACCOUNT"))
    async def account(self, inter: AppCmdInter,
                      user: disnake.User = commands.Param(
                          name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                          description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
                          default=lambda inter: inter.author
                      )
    ):
        locale = _(inter.locale, "account")

        await acc(locale=locale, client=self.client, inter=inter, user=user)
        

    @commands.user_command(name=__("user", key="COMMAND_NAME_ACCOUNT_USER-COMMAND"))
    async def _account(self, inter: UserCommandInteraction, user: disnake.User):
        locale = _(inter.locale, "account")

        await acc(locale=locale, client=self.client, inter=inter, user=user)
    
def setup(client: commands.InteractionBot):
    client.add_cog(Accounts(client))