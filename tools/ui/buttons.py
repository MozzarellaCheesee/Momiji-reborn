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