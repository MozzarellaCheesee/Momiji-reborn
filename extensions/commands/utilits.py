import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage

class Utilits(BaseCog):

    @commands.slash_command(name=__("utilits", key="COMMAND_GROUP_UTILITS"))
    async def utilits():
        ...

def setup(client: commands.InteractionBot):
    client.add_cog(Utilits(client))