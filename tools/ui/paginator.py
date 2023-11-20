import disnake

class Paginator(disnake.ui.View):

    def __init__(self, *,
                 pages: list[disnake.Embed],
                 inter: disnake.ApplicationCommandInteraction = None,
                 inter_resp: disnake.MessageInteraction = None,
                 timeout: float = 180.0,
                 ephemeral: bool = False,
                 childrens: list = None) -> None:
        super().__init__(timeout=timeout)
        self._inter = inter
        self._pages = pages
        self.ephemeral = ephemeral
        self.first.disabled = True
        self.last.disabled = False
        self.inter_resp = inter_resp
        self.page_index = 0
        self.childrens = childrens

        if self.childrens is not None:
            for children in self.childrens:
                self.add_item(children)

    async def on_timeout(self) -> None:
        try:
            try:
                try:
                    for button in self.children:
                        button.disabled = True
                    await self._inter.edit_original_message(view=self)
                    return await super().on_timeout()
                except:
                    for button in self.children:
                        button.disabled = True
                    await self.inter_resp.response.edit_message(view=self)
                    return await super().on_timeout()
            except:
                return
        except disnake.errors.HTTPException:
            return
        except disnake.errors.NotFound:
            return

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        try:
            return interaction.user == self._inter.author
        except:
            return interaction.user == self.inter_resp.author


    @disnake.ui.button(label="⏪")
    async def first(self, button, inter):
        self.page_index = 0
        embed = self._pages[0]
        self.first.disabled = True
        self.next.disabled = False
        self.previous.disabled = True
        self.last.disabled = False

        await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="◀", style=disnake.ButtonStyle.blurple)
    async def previous(self, button, inter):
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
        await inter.response.defer()
        await inter.delete_original_message()

    @disnake.ui.button(label="▶", style=disnake.ButtonStyle.blurple)
    async def next(self, button, inter):
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
        self.page_index = len(self._pages) - 1
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

    async def start_resp(self, text: str = None):

        await self.inter_resp.response.send_message(content=text, embed=self._pages[0], view=self, ephemeral=self.ephemeral)

    async def start_edit_resp(self, text: str = None):

        await self.inter_resp.response.edit_message(content=text, embed=self._pages[0], view=self)