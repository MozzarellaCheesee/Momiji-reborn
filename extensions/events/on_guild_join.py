from extensions.events.__init__ import *

class GuildJoin(BaseCog):

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):

        server_in_db = await self.client.db.Servers.get_or_create(discord_id=guild.id)

        for member in guild.members:
            defauilts = {
            "discord_id": member.id
            }
            if not member.bot:
                user_in_db = await self.client.db.Users.get_or_create(defaults=defauilts, discord_id=member.id)
                if await self.client.db.Profiles.get_or_none(user=user_in_db[0], server=server_in_db[0]) is None:
                    await self.client.db.Profiles.create(user=user_in_db[0], server=server_in_db[0], family=None)



def setup(client: commands.InteractionBot):
    client.add_cog(GuildJoin(client))
