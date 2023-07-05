import disnake
import traceback
import dataclasses
from disnake.ext import commands

from core.i18n import LocalizationStorage
from tools.exeption import CustomError
from tools.ui.buttons import SupportButton

from tortoise.models import Model

from core.cog import BaseCog
from core.models.authorized_sessions import AuthorizedSessions
from core.models.banks import Banks
from core.models.channels import Channels
from core.models.families import Families
from core.models.profiles import Profiles
from core.models.servers import Servers
from core.models.tickets import Tickets
from core.models.users import Users
from core.models.warns import Warns