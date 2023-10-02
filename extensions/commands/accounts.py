import disnake
from disnake import AppCmdInter, UserCommandInteraction
from disnake.i18n import Localised as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from tools.utils import account as acc
from tools.exeption import CustomError


_ = LocalizationStorage("user")
err = LocalizationStorage('errors#2')


class Accounts(BaseCog):

    # @commands.slash_command()
    
    @commands.slash_command(name=__("account", key="COMMAND_NAME_ACCOUNT"),
                            description=__("User account in the bot system", key="COMMAND_DESCRIPTION_ACCOUNT"))
    async def account(self, inter: AppCmdInter,
                      user: disnake.User = commands.Param(
                        name=__("user", key="COMMAND_PARAM_NAME_USER"),
                        description=__("select user", key="COMMAND_PARAM_DESCRIPTION_USER"),
                        default=lambda inter: inter.author,

                      )
    ):
        locale = _(inter.locale, "account")
        loc = err(inter.locale, "errors")
        if user.bot:
            raise CustomError(loc['bot_error'])

        await acc(locale=locale, client=self.client, inter=inter, user=user)
        

    @commands.user_command(name=__("Account", key="COMMAND_NAME_ACCOUNT_USER_COMMAND"))
    async def _account(self, inter: UserCommandInteraction, user: disnake.User):
        locale = _(inter.locale, "account")
        loc = err(inter.locale, "errors")
        if user.bot:
            raise CustomError(loc['bot_error'])

        await acc(locale=locale, client=self.client, inter=inter, user=user)
    
def setup(client: commands.InteractionBot):
    client.add_cog(Accounts(client))