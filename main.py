import disnake
from disnake.ext import commands
from pathlib import Path

from core.settings import commands_, events
from core.database import init_database
from core.settings import config

localization_path = Path("./locale/commands")

client = commands.InteractionBot(intents=disnake.Intents.all())

def load_extensions():
    for command in commands_:
        try:
            client.load_extension(command)
        except Exception as e:
            print(f"[ERROR] | Ошибка при загрузке команд: {e}")

    for event in events:
        try:
            client.load_extension(event)
        except Exception as e:
            print(f"[ERROR] | Ошибка при загрузке ивентов: {e}")

def load_locale():
    for dir_ in localization_path.iterdir():
        if dir_.is_dir():
            client.i18n.load(dir_)

async def main():
    load_extensions()
    load_locale()
    await init_database()
    await client.start(config["TOKEN"])

if __name__ == "__main__":
    client.loop.run_until_complete(main())
    del client, commands_, events, localization_path