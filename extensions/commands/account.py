import disnake
from disnake import AppCmdInter, UserCommandInteraction
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage


_ = LocalizationStorage("profile")

class Profile(BaseCog):
    ...
    
def setup(client: commands.InteractionBot):
    client.add_cog(Profile(client))