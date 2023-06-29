import disnake

embeds = []

class Paginator(disnake.ui.View):

    def __init__(self, *,
                 pages: list[disnake.Embed],
                 inter: disnake.ApplicationCommandInteraction,
                 timeout: float = 180.0,
                 ephemeral: bool = False) -> None:
        super().__init__(timeout=timeout)
        self._inter = inter
        self._author = inter.author.id
        self._pages = pages
        self.ephemeral = ephemeral
        self.first.disabled = True
        self.last.disabled = False
        self.page_index = 0

    @disnake.ui.button(label="⏪")
    async def first(self, button, inter):
        if inter.author.id == self._author:
            embed = self._pages[0]
            self.first.disabled = True
            self.next.disabled = False
            self.previous.disabled = True
            self.last.disabled = False

            await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="◀", style=disnake.ButtonStyle.blurple)
    async def previous(self, button, inter):
        if inter.author.id == self._author:
            self.page_index -= 1
            embed = self._pages[self.page_index]

            self.next.disabled = False
            self.last.disabled = False

            if self.page_index == 0:
                self.first.disabled = True
                self.previous.disabled = True

            await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji='❌')
    async def close(self, button, inter):
        if inter.author.id == self._author:
            await inter.response.defer()
            await inter.delete_original_message()

    @disnake.ui.button(label="▶", style=disnake.ButtonStyle.blurple)
    async def next(self, button, inter):
        if inter.author.id == self._author:
            self.page_index += 1
            embed = self._pages[self.page_index]

            self.first.disabled = False
            self.previous.disabled = False

            if self.page_index == len(self._pages) - 1:
                self.next.disabled = True
                self.last.disabled = True

            await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="⏩")
    async def last(self, button, inter):
        if not inter.author.id == self._author:
            embed = self._pages[-1]
            self.last.disabled = True
            self.next.disabled = True
            self.previous.disabled = False
            self.first.disabled = False

            await inter.response.edit_message(embed=embed, view=self)

    async def start(self, text: str = None):
        """
        Отправляет пагинатор

        :return:
        """

        await self._inter.send(content=text, embed=self._pages[0], view=self, ephemeral=self.ephemeral)