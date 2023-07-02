import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage

from tools.ui.modals import ReportModal

_ = LocalizationStorage("utilits")


class Utilits(BaseCog):

    @commands.slash_command(name=__("utilits", key="COMMAND_GROUP_UTILITS"))
    async def utilits(self, inter:AppCmdInter):
       ...

    @commands.cooldown(1, 240, commands.BucketType.user)
    @utilits.sub_command()
    async def report(self, inter: AppCmdInter):
        locale = _(inter.locale, "report")
        await inter.response.send_modal(modal=ReportModal(locale=locale, bot=self.client, interaction=inter))

def setup(client: commands.InteractionBot):
    client.add_cog(Utilits(client))