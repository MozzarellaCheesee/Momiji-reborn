import disnake


class SupportButton(disnake.ui.View):
    
    def __init__(self):
        super().__init__()

    @disnake.ui.button(
        label="Support server", 
        style=disnake.ButtonStyle.blurple,
        emoji="✨"
    )
    async def support_server(self, button, inter):
        await inter.response.send_message("Support server: https://discord.gg/WgUU4zkDhY", ephemeral=True)


class InfoButtons(disnake.ui.View):

    def __init__(self):
        super(InfoButtons, self).__init__(timeout=None)

    @disnake.ui.button(label="Boosty", url="https://boosty.to/your-reimu-bot", style=disnake.ButtonStyle.grey)
    async def boosty(self, button, inter):
        ...

    @disnake.ui.button(label="Donate", url="https://boosty.to/your-reimu-bot/donate", style=disnake.ButtonStyle.grey)
    async def bonate(self, button, inter):
        ...

    @disnake.ui.button(
        label="Support server",
        style=disnake.ButtonStyle.grey,
        emoji="✨"
    )
    async def support_info_server(self, button, inter):
        await inter.response.send_message("Support server: https://discord.gg/WgUU4zkDhY", ephemeral=True)