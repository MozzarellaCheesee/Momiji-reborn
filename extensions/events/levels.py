import disnake
from disnake.ext import commands
from random import randint

from core.cog import BaseCog
from asyncmy.errors import OperationalError


class Level(BaseCog):

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return
        try:
            user = await self.client.db.Users.get_or_create(discord_id=message.author.id)
            server = await self.client.db.Servers.get_or_create(discord_id=message.guild.id)
            profile = await self.client.db.Profiles.get_or_none(user=user[0], server=server[0])
            user[0].messages += 1

            if len(message.content) > 5:
                rand_xp = randint(1, 7)

                if profile is not None:
                    profile.messages += 1
                    new_profile_lvl = profile.level * 50
                    profile.experience += rand_xp

                    if profile.experience >= new_profile_lvl:
                        profile.level += 1
                        profile.experience = 0
                    await profile.save()

                new_user_lvl = user[0].level * 50
                user[0].experience += rand_xp

                if user[0].experience >= new_user_lvl:
                    user[0].level += 1
                    user[0].experience = 0

            await user[0].save()
        except AttributeError:
            ...
        except OperationalError:
            ...


def setup(client: commands.InteractionBot):
    client.add_cog(Level(client))
