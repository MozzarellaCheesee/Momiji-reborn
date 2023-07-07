import disnake
from disnake.ext import commands
from random import randint

from core.cog import BaseCog
from tools.utils import get_member_profile

class Level(BaseCog):

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        profile = await get_member_profile(message.author, self.client)
        profile.messages = profile.messages + 1
        
        if len(message.content) > 5:
            new_lvl = profile.level * 50
            profile.experience = profile.experience + randint(1, 7)

            if profile.experience >= new_lvl:
                profile.level = profile.level + 1
                profile.experience = 0
            
        await profile.save()

def setup(client: commands.InteractionBot):
    client.add_cog(Level(client))