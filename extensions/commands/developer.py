import disnake
from disnake import AppCmdInter
from disnake.ext import commands

from core.cog import BaseCog

class Developer(BaseCog):

    ...
        


def setup(client: commands.InteractionBot):
    client.add_cog(Developer(client))