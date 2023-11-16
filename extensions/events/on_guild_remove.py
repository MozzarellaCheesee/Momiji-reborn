import disnake
from disnake.ext import commands

from core.cog import BaseCog


class GuildRemove(BaseCog):

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: disnake.Guild):
        await self.client.db.Servers.filter(discord_id=guild.id).delete()

        await self.client.channels.log_remove_channel.send(
            f"Бот успешно вышел с сервера `{guild.name}`! Owner: {guild.owner.mention} ({guild.owner.name}) | Members count: {guild.member_count}"
        )


def setup(client: commands.InteractionBot):
    client.add_cog(GuildRemove(client))
