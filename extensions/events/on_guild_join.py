import disnake
from disnake.ext import commands

from core.cog import BaseCog


class GuildJoin(BaseCog):

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        await self.client.db.Servers.get_or_create(discord_id=guild.id)

        await self.client.channels.log_join_channel.send(
            f"Бот успешно присоединился к серверу `{guild.name}`! Owner: {guild.owner.mention} ({guild.owner.name}) | \
            Members count: {guild.member_count}"
        )


def setup(client: commands.InteractionBot):
    client.add_cog(GuildJoin(client))
