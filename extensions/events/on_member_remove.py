import disnake
from disnake.ext import commands

from core.cog import BaseCog


class MemberRemove(BaseCog):

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.bot:
            return

        user_in_db = await self.client.db.Users.get_or_create(discord_id=member.id)
        server_in_db = await self.client.db.Servers.get_or_create(discord_id=member.guild.id)
        await self.client.db.Profiles.filter(user=user_in_db, server=server_in_db).delete()


def setup(client: commands.InteractionBot):
    client.add_cog(MemberRemove(client))
