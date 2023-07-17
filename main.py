import disnake
from disnake.ext import commands
from pathlib import Path
import logging

from core.settings import commands_, events
from core.database import init_database
from core.settings import config

localization_path = Path("./locale/commands")
logging.basicConfig(
    filename='logs/info.log', 
    encoding='utf-8', 
    level=logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)

client = commands.InteractionBot(intents=disnake.Intents.all(), strict_localization=True)

def load_extensions():
    for command in commands_:
        try:
            client.load_extension(command)
        except Exception as e:
            print(
                f"\033[31;1;31m[ERROR] \033[0;0m| Ошибка при загрузке команд: \033[33;1;33m{e}\033[0;0m\n"
                f"----------------------------------------------"
            )

    for event in events:
        try:
            client.load_extension(event)
        except Exception as e:
            print(
                f"\033[31;1;31m[ERROR] \033[0;0m| Ошибка при загрузке ивентов: \033[33;1;33m{e}\033[0;0m\n"
                f"----------------------------------------------"
            )
    logging.info("Компоненты загружены")

def load_locale():
    for dir_ in localization_path.iterdir():
        if dir_.is_dir():
            client.i18n.load(dir_)
    logging.info("Локализация для аргументов и названий команд загружена")

async def main():
    load_locale()
    await init_database()
    load_extensions()
    await client.start(config["TOKEN"])

if __name__ == "__main__":
    logging.info("Загрузка основных модулей начата")
    client.loop.run_until_complete(main())
    del client, commands_, events, localization_path