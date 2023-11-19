import disnake
from disnake import AppCmdInter
from disnake.ext import commands

from core.cog import BaseCog
from tools.ui.components import StandartView, StandardSelect

from core.settings import commands_, events


class ReloadCogs(StandardSelect):
    def __init__(self, cogs_list: list):
        super().__init__(placeholder='select cogs to reload', options=cogs_list, row=1, max_values=len(cogs_list))

    async def callback(self, interaction: disnake.MessageInteraction) -> None:
        await interaction.response.defer()
        for cogs in interaction.values:
            self.view.client.reload_extension(cogs)
        await interaction.edit_original_message(
            embed=disnake.Embed(
                title='reload cogs',
                description='\n '.join(interaction.values)
            )
        )


class Developer(BaseCog):

    @commands.is_owner()
    @commands.slash_command(name="разблокировать",
                            description='ТОЛЬКО ВЛАДЕЛЕЦ БОТА! Разблокировать пользователя в системе')
    async def unblock(self, inter: AppCmdInter, user: disnake.User):
        user = await self.client.db.Users.get_or_create(discord_id=user.id)
        if user[0].status != "BLOCKED":
            await inter.send('Пользователь не заблокирован', ephemeral=True)
            return

        user[0].status = None
        await user[0].save()
        await inter.send('Пользователь был разблокирован', ephemeral=True)

    @commands.is_owner()
    @commands.slash_command(name="заблокировать",
                            description='ТОЛЬКО ВЛАДЕЛЕЦ БОТА! Заблокировать пользователя в системе')
    async def block(self, inter: AppCmdInter, user: disnake.User):
        user = await self.client.db.Users.get_or_create(discord_id=user.id)
        if user[0].status == "BLOCKED":
            await inter.send('Пользователь уже заблокирован', ephemeral=True)
            return

        user[0].status = "BLOCKED"
        await user[0].save()
        await inter.send('Пользователь был заблокирован', ephemeral=True)

    @commands.is_owner()
    @commands.slash_command(name="перезагрузка", description='ТОЛЬКО ВЛАДЕЛЕЦ БОТА! Перезагрузка модулей бота')
    async def reload(self, inter: AppCmdInter):
        view = StandartView(inter, self.client, timeout=60)
        view.add_item(ReloadCogs(list(list(commands_) + list(events))))
        await inter.send(
            embed=disnake.Embed(
                title="Reload cogs"
            ), view=view
        )


def setup(client: commands.InteractionBot):
    client.add_cog(Developer(client))
