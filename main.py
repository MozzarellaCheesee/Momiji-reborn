import disnake
from boticordpy import BoticordClient
from disnake.ext import commands

from core.database import init_database
from core.settings import config
from tools.system_utils import load_extensions, load_locale, get_stats, on_success_posting

client = commands.AutoShardedInteractionBot(intents=disnake.Intents.all(), strict_localization=True)
boticord_client: BoticordClient = BoticordClient(config['BOTICORD_TOKEN'], version=3)


async def main():
    load_locale(client)
    load_extensions(client)
    await init_database()
    await client.start(config["MOMIJI_TOKEN"])


if __name__ == "__main__":
    boticord_client.autopost().init_stats(get_stats(client)).on_success(on_success_posting()).start(config['MOMIJI_TOKEN'])
    client.loop.run_until_complete(main())
