import disnake
from disnake.ext import commands

from core.cog import BaseCog

class BotActivity(BaseCog):

    @commands.Cog.listener(name="Activity")
    async def on_ready(self):
        print(f"{self.client.user} is worked stable.")
        await self.client.change_presence(activity=disnake.Streaming(name="Waiting for new members..", url="https://www.twitch.tv/astolfo_oxo"))

def setup(client: commands.InteractionBot):
    client.add_cog(BotActivity(client))