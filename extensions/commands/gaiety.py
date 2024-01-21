import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands
from random import randint

from core.cog import BaseCog
from core.i18n import LocalizationStorage

_ = LocalizationStorage("gaiety")


class Gaiety(BaseCog):

    @commands.slash_command(name=__("gaiety", key="COMMAND_GROUP_GAIETY"),
                            description=__("gaiety's commands", key="COMMAND_GROUP_DESCRIPTION_GAIETY"))
    async def gaiety(self, inter: AppCmdInter):
        ...

    @gaiety.sub_command(name='8ball',
                        description=__('ask the ball about what worries you', key="COMMAND_DESCRIPTION_8BALL"))
    async def _8ball(self, inter: AppCmdInter,
                     question: str = commands.Param(
                         name=__("question", key="COMMAND_PARAM_NAME_QUEST"),
                         description=__("enter your question", key="COMMAND_PARAM_DESCRIPTION_QUEST")
                     )
    ):
        locale = _(inter.locale, "8ball")
        answer = randint(1, 20)
        await inter.send(
            embed=disnake.Embed(
                title=locale["title"],
                description=locale[f"{answer}"]
            )
        )


def setup(client: commands.InteractionBot):
    client.add_cog(Gaiety(client))
