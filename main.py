from pathlib import Path

import disnake
from disnake.ext import commands

from core.settings import commands_, events

from dotenv import load_dotenv
from os import getenv



localization_path = Path("./locale/commands")

client = commands.InteractionBot(intents=disnake.Intents.all())

@client.event
async def on_ready():
    print(f"{client.user} is worked stable.")
    await client.change_presence(activity=disnake.Streaming(name="Waiting for new members..", url="https://www.twitch.tv/astolfo_oxo"))

def load_extensions():
    for command in commands_:
        try:
            client.load_extension(command)
        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке команд: {e}")

    for event in events:
        try:
            client.load_extension(event)
        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке ивентов: {e}")

    

def load_locale():
    for dir_ in localization_path.iterdir():
        if dir_.is_dir():
            client.i18n.load(dir_)

def main():
    load_extensions()
    load_locale()
    load_dotenv()
    client.run(getenv("TOKEN"))

    

if __name__ == "__main__":
    client.loop.run_until_complete(main())
    del client, commands_, events, localization_path