import disnake
from disnake.ext import commands
from random import uniform

from core.cog import BaseCog
from tools.utils import lvl_check
import tortoise


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
                if len(message.content) > 150:
                    rand_xp_coef = uniform(0.1, 0.3)
                    del_coef = uniform(5, 7)
                else:
                    rand_xp_coef = uniform(1.1, 1.5)
                    del_coef = uniform(1, 2)
                new_user_lvl_xp = user[0].level * 50

                if profile is not None:
                    new_profile_lvl_xp = profile.level * 50
                    profile.messages += 1
                    profile.experience += (int(rand_xp_coef * (len(message.content)//del_coef)))

                    if profile.experience >= new_profile_lvl_xp:
                        lvl_exp = lvl_check(profile.experience, new_profile_lvl_xp)
                        profile.level += lvl_exp[0]
                        profile.experience = lvl_exp[1]

                    await profile.save()

                user[0].experience += (int(rand_xp_coef * (len(message.content)//del_coef)))
                if user[0].experience >= new_user_lvl_xp:
                    lvl_exp = lvl_check(user[0].experience, new_user_lvl_xp)
                    user[0].level += lvl_exp[0]
                    user[0].experience = lvl_exp[1]

                await user[0].save()
        except AttributeError:
            ...
        except tortoise.exceptions.OperationalError:
            ...


def setup(client: commands.InteractionBot):
    client.add_cog(Level(client))
