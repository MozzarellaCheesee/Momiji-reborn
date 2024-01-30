import disnake
from disnake.ext import commands


class StandartView(disnake.ui.View):

    def __init__(self, inter, client: commands.InteractionBot, timeout: float = 45):
        super().__init__(timeout=timeout)
        self.flag = 0
        self.inter = inter
        self.client = client

    async def on_timeout(self) -> None:
        if self.flag == 0:
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


class StandartButton(disnake.ui.Button):
    view: StandartView


class StandardSelect(disnake.ui.Select):
    view: StandartView


class BackButton(StandartButton):
    def __init__(self, emb, children, locale):
        super().__init__(label=locale['back'], row=4, style=disnake.ButtonStyle.red,
                         emoji="<:back:1200744962334142626>")
        self.emb = emb
        self.children = children

    async def callback(self, interaction: disnake.MessageInteraction) -> None:
        self.view.clear_items()
        for x in self.children:
            self.view.add_item(x)
        await interaction.response.edit_message(embed=self.emb, view=self.view)
