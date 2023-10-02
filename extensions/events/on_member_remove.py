from extensions.events.__init__ import *

class MemberRemove(BaseCog):

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.bot:
            return

        user_in_db = await self.client.db.Users.get(discord_id=member.id)
        server_in_db = await self.client.db.Servers.get(discord_id=member.guild.id)
        await self.client.db.Profiles.filter(user=user_in_db, server=server_in_db).delete()



def setup(client: commands.InteractionBot):
    client.add_cog(MemberRemove(client))
