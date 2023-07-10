from extensions.events.__init__ import *

class GuildRemove(BaseCog):

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: disnake.Guild):
        await self.client.db.Servers.filter(discord_id=guild.id).delete()



def setup(client: commands.InteractionBot):
    client.add_cog(GuildRemove(client))
