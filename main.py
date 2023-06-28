from pathlib import Path

import disnake
from disnake.ext import commands

from dotenv import load_dotenv
from os import getenv, listdir



localization_path = Path("./locale/commands")

client = commands.InteractionBot(intents=disnake.Intents.all())

@client.event
async def on_ready():
    print(f"{client.user} is worked stable.")
    await client.change_presence(activity=disnake.Streaming(name="Waiting for new members..", url="https://www.twitch.tv/astolfo_oxo"))

def load_extensions():
    for extension_type in listdir("./extensions"):
        for extension in listdir(f"./extensions/{extension_type}"):
            if extension.endswith(".py"):
                try:
                    client.load_extension(f"extensions.{extension_type}.{extension[:-3]}")
                except Exception as e:
                    print(e)

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

