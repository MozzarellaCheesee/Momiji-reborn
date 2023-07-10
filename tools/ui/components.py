import disnake
from disnake.ext import commands

class StandartView(disnake.ui.View):

    def __init__(self, inter, client: commands.InteractionBot, timeout: float = 45):
        super().__init__(timeout=timeout)

        self.inter = inter
        self.client = client

    async def on_timeout(self) -> None:
        try:
            for button in self.children:
                button.disabled = True
            await self.inter.edit_original_message(view=self)
            return await super().on_timeout()
        except disnake.errors.NotFound:
            return
        except disnake.errors.HTTPException:
            return

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return interaction.user == self.inter.author

class StandardButton(disnake.ui.Button):
    view: StandartView


class StandardSelect(disnake.ui.Select):
    view: StandartView


class BackButton(StandardButton):
    def __init__(self, emb, children):
        super().__init__(label='Назад', row=4)
        self.emb = emb
        self.children = children

    async def callback(self, interaction: disnake.MessageInteraction) -> None:
        self.view.clear_items()
        for x in self.children:
            self.view.add_item(x)
        await interaction.response.edit_message(embed=self.emb, view=self.view)