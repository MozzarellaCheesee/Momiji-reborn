import disnake
from disnake import AppCmdInter
from disnake.ext import commands

from core.cog import BaseCog

class Developer(BaseCog):

    @commands.is_owner()
    @commands.slash_command()
    async def unblock(self, inter: AppCmdInter, user: disnake.User):
        user = await self.client.db.Users.get(discord_id=user.id)
        if user.status != "BLOCKED":
            await inter.send('Пользователь не заблокирован', ephemeral=True)
            return
        
        user.status = None
        await user.save()
        await inter.send('Пользователь был разблокирован', ephemeral=True)

    @commands.is_owner()
    @commands.slash_command()
    async def block(self, inter: AppCmdInter, user: disnake.User):
        user = await self.client.db.Users.get(discord_id=user.id)
        if user.status == "BLOCKED":
            await inter.send('Пользователь уже заблокирован', ephemeral=True)
            return
        
        user.status = "BLOCKED"
        await user.save()
        await inter.send('Пользователь был заблокирован', ephemeral=True)


def setup(client: commands.InteractionBot):
    client.add_cog(Developer(client))