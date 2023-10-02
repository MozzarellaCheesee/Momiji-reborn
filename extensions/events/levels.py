import disnake
from disnake.ext import commands
from random import randint

from core.cog import BaseCog
from tools.utils import get_member_profile

class Level(BaseCog):

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        try:
            user = await self.client.db.Users.get(discord_id=message.author.id)
            profile = await get_member_profile(message.author, self.client)
            profile.messages += 1
            user.messages += 1
            
            if len(message.content) > 5:
                new_lvl = profile.level * 50
                new_user_lvl = user.level * 50
                rand_xp = randint(1, 7)
                profile.experience += rand_xp
                user.experience += rand_xp

                if profile.experience >= new_lvl:
                    profile.level += 1
                    profile.experience = 0

                if user.experience >= new_user_lvl:
                    user.level += 1
                    user.experience = 0

                
            await profile.save()
            await user.save()
        except:
            ...

def setup(client: commands.InteractionBot):
    client.add_cog(Level(client))