from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage

from tools.ui.modals import ReportModal, IdeaModal
from tools.exeption import CustomError

_ = LocalizationStorage("utilits")


class Utilits(BaseCog):

    @commands.slash_command(name=__("utilits", key="COMMAND_GROUP_UTILITS"),
                            description=__("utilit commands", key="COMMAND_GROUP_DESCRIPTION_UTILITS"))
    async def utilits(self, inter: AppCmdInter):
       ...

    @commands.cooldown(1, 240, commands.BucketType.user)
    @utilits.sub_command(name=__("report", key="COMMAND_NAME_REPORT"),
                         description=__("send report", key="COMMAND_DESCRIPTION_REPORT"))
    async def report(self, inter: AppCmdInter):
        locale = _(inter.locale, "report")
        user = await self.client.db.Users.get(discord_id=inter.author.id)
        if user.status == "BLOCKED":
            raise CustomError(locale['error'])
        await inter.response.send_modal(modal=ReportModal(locale=locale, bot=self.client, interaction=inter))

    @commands.cooldown(1, 240, commands.BucketType.user)
    @utilits.sub_command(name=__("idea", key="COMMAND_NAME_IDEA"),
                         description=__("send idea", key="COMMAND_DESCRIPTION_IDEA"))
    async def idea(self, inter: AppCmdInter):
        locale = _(inter.locale, "idea")
        user = await self.client.db.Users.get(discord_id=inter.author.id)
        if user.status == "BLOCKED":
            raise CustomError(locale["error"])
        await inter.response.send_modal(modal=IdeaModal(locale=locale, bot=self.client, interaction=inter))

def setup(client: commands.InteractionBot):
    client.add_cog(Utilits(client))