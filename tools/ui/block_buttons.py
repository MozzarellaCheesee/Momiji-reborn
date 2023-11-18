import disnake


class BlockButton(disnake.ui.View):
    def __init__(self, user, client, embed):
        self.client = client
        self.user = user
        self.embed = embed
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="ЗАБЛОКИРОВАТЬ",
        style=disnake.ButtonStyle.red
    )
    async def a_callback(self, button: disnake.Button, inter: disnake.Interaction):
        user = await self.client.db.Users.get_or_create(discord_id=self.user.id)
        user.status = 'BLOCKED'
        await user.save()
        await inter.response.edit_message(embed=self.embed, view=UnBlockButton(self.user, self.client, self.embed))


class UnBlockButton(disnake.ui.View):
    def __init__(self, user, client, embed):
        self.client = client
        self.user = user
        self.embed = embed
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="РАЗБЛОКИРОВАТЬ",
        style=disnake.ButtonStyle.green
    )
    async def a_callback(self, button: disnake.Button, inter: disnake.Interaction):
        user = await self.client.db.Users.get_or_create(discord_id=self.user.id)
        user.status = None
        await user.save()
        await inter.response.edit_message(embed=self.embed, view=BlockButton(self.user, self.client, self.embed))
