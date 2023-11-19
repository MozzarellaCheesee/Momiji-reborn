import disnake
from disnake.ext import commands

from core.database import init_database
from core.settings import config
from tools.system_utils import load_extensions, load_locale

client = commands.InteractionBot(intents=disnake.Intents.all(), strict_localization=True)


async def main():
    load_locale(client)
    load_extensions(client)
    await init_database()
    await client.start(config["MOMIJI_TOKEN"])


if __name__ == "__main__":
    client.loop.run_until_complete(main())
