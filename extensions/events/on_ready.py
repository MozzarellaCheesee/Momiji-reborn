import disnake
from disnake.ext import commands

from core.cog import BaseCog


class BotActivity(BaseCog):

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.on_error_channel = self.client.get_channel(985268089174233180)
        self.client.report_channel = self.client.get_channel(1125118943959453768)
        print(f"{self.client.user} is worked stable.")
        await self.client.change_presence(
            activity=disnake.Streaming(name="Waiting for new members..", url="https://www.twitch.tv/astolfo_oxo"))

def setup(client: commands.InteractionBot):
    client.add_cog(BotActivity(client))
