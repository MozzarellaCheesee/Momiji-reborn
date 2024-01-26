import disnake
from disnake.ext import commands

from core.i18n import LocalizationStorage
from core.cog import BaseCog
from tools.ui.modals.server_settings_verefy import VerefyButton

import logging
import dataclasses

from tortoise.models import Model

from core.models.authorized_sessions import AuthorizedSessions
from core.models.channels import Channels
from core.models.families import Families
from core.models.private_vc import PrivateVCS
from core.models.profiles import Profiles
from core.models.servers import Servers
from core.models.tickets import Tickets
from core.models.users import Users
from core.models.warns import Warns
from core.models.roles import Roles

_ = LocalizationStorage("server_settings")


class OnReady(BaseCog):

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Загрузка клиента")

        @dataclasses.dataclass
        class Models:
            AuthorizedSessions: Model = AuthorizedSessions
            Channels: Model = Channels
            Families: Model = Families
            PrivateVCS: Model = PrivateVCS
            Profiles: Model = Profiles
            Servers: Model = Servers
            Tickets: Model = Tickets
            Users: Model = Users
            Warns: Model = Warns
            Roles: Model = Roles

        @dataclasses.dataclass
        class Channels:
            on_error_channel = self.client.get_channel(985268089174233180)
            report_channel = self.client.get_channel(1125118943959453768)
            idea_channel = self.client.get_channel(1125118961978183790)
            log_join_channel = self.client.get_channel(978325826753953975)
            log_remove_channel = self.client.get_channel(978620072014782515)

        @dataclasses.dataclass
        class Emojies:
            messages_emoji = self.client.get_emoji(1127503836429438976)
            money_emoji = self.client.get_emoji(1126456975337730078)
            level_emoji = self.client.get_emoji(1127504341482344489)

        self.client.channels = Channels
        self.client.db = Models
        self.client.emojies = Emojies

        await self.client.change_presence(
            activity=disnake.Streaming(name="Waiting for new members..", url="https://www.twitch.tv/astolfo_oxo"))

        self.client.add_view(view=VerefyButton(self.client, _))

        print(
            f"\033[38;5;38m[CLIENT] \033[38;5;67m⌗ \033[38;5;105m{self.client.user}\033[0;0m is worked stable.\n"
            f"----------------------------------------------"
        )
        logging.info("Бот был запущен")

    @commands.Cog.listener()
    async def on_disconnect(self):
        print(
            f"\033[38;5;38m[DISCONNECT] \033[38;5;67m⌗ \033[38;5;105m{self.client.user}\033[0;0m is disconnected.\n"
            f"----------------------------------------------"
        )

    @commands.Cog.listener()
    async def on_connect(self):
        print(
            f"\033[38;5;38m[CONNECT] \033[38;5;67m⌗ \033[38;5;105m{self.client.user}\033[0;0m is connected.\n"
            f"----------------------------------------------"
        )


def setup(client: commands.InteractionBot):
    client.add_cog(OnReady(client))
