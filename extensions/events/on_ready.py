import disnake
from disnake.ext import commands

from core.i18n import LocalizationStorage
from core.cog import BaseCog

from tools.dataclasses import Models
from tools.ui.modals.server_settings_verefy import VerefyButton

import logging
import dataclasses

_ = LocalizationStorage("server_settings")


class OnReady(BaseCog):

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Загрузка клиента")

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

        for user in self.client.users:
            if not user.bot:
                await self.client.db.Users.get_or_create(discord_id=user.id)
                logging.info(f"Пользователь {user.name} | {user.id} успешно найден/добавлен в базе(-у) данных")

        for guild in self.client.guilds:
            server_in_db = await self.client.db.Servers.get_or_create(discord_id=guild.id)
            logging.info(f"Сервер {guild.name} | {guild.id} успешно найден/добавлен в базе(-у) данных")
            for member in guild.members:
                if not member.bot:
                    user_in_db = await self.client.db.Users.get(discord_id=member.id)
                    if await self.client.db.Profiles.get_or_none(server=server_in_db[0], user=user_in_db) is None:
                        await self.client.db.Profiles.create(user=user_in_db, server=server_in_db[0])

        await self.client.change_presence(
            activity=disnake.Streaming(name="Waiting for new members..", url="https://www.twitch.tv/astolfo_oxo"))

        self.client.add_view(view=VerefyButton(self.client, _))

        print(
            f"\033[38;5;38m[CLIENT] \033[38;5;67m⌗ \033[38;5;105m{self.client.user}\033[0;0m is worked stable.\n"
            f"----------------------------------------------"
        )
        logging.info("Бот был запущен")


def setup(client: commands.InteractionBot):
    client.add_cog(OnReady(client))
