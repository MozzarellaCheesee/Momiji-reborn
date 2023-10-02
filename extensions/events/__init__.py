import disnake
import traceback
import dataclasses
from disnake.ext import commands

import logging

from core.i18n import LocalizationStorage
from tools.exeption import CustomError
from tools.ui.buttons import SupportButton
from tools.utils import standard_emb
from tools.ui.modals.server_settings_verefy import VerefyButton

from tortoise.models import Model

from core.cog import BaseCog
from core.models.authorized_sessions import AuthorizedSessions
from core.models.channels import Channels
from core.models.families import Families
from core.models.profiles import Profiles
from core.models.servers import Servers
from core.models.tickets import Tickets
from core.models.users import Users
from core.models.warns import Warns
from core.models.roles import Roles
from main import client