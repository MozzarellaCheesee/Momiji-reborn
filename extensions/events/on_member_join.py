from extensions.events.__init__ import *

class MemberJoin(BaseCog):

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if member.bot:
            return

        user_in_db = await self.client.db.Users.get(discord_id=member.id)
        server_in_db = await self.client.db.Servers.get(discord_id=member.guild.id)
        await self.client.db.Profiles.create(user=user_in_db, server=server_in_db, family=None)



def setup(client: commands.InteractionBot):
    client.add_cog(MemberJoin(client))
