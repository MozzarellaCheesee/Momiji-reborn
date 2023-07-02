import disnake
from disnake.ui import Modal, TextInput
from disnake import TextInputStyle, ModalInteraction
from tools.ui.buttons import SupportButton

class ReportModal(Modal):
    
    def __init__(self, locale: dict, bot: disnake.ext.commands.bot.InteractionBot, interaction: disnake.AppCmdInter) -> None:
        self.locale = locale
        self.bot = bot
        self.interaction = interaction
        components = [
            TextInput(
                label=f"{locale['textinput_label_1']}",
                placeholder=f"{locale['textinput_placeholder_1']}",
                custom_id="description",
                style=TextInputStyle.paragraph
            ),
            TextInput(
                label=f"{locale['textinput_label_2']}",
                placeholder=f"{locale['textinput_placeholder_2']}",
                custom_id="image",
                style=TextInputStyle.short,
                required=False
            )
        ]

        super().__init__(title=f"{locale['modal_title']}", 
                         components=components,
                         custom_id="report_modal",
                         timeout=300)

    async def callback(self, inter: ModalInteraction) -> None:

        dev_embed = disnake.Embed(
            title="Новый репорт!",
            description=f"Пришёл новый репорт с сервера `{self.interaction.guild.name}`"
        ).add_field(
            name="Ошибку нашел:",
            value=f"{self.interaction.author.mention}\n`{self.interaction.author}`"
        ).add_field(
            name="Описание ошибки:",
            value=inter.text_values["description"]
        )

        user_embed = disnake.Embed(
            title=self.locale["embed_title"],
            description=self.locale["embed_descriprion"]
        )

        if inter.text_values["image"] and "https://" in inter.text_values["image"]:
            dev_embed.add_field(
                name="Скрин",
                value=f"[Клик...]({inter.text_values['image']})"
            )

        await inter.response.send_message(embed=user_embed, ephemeral=True, view=SupportButton())
        await self.bot.report_channel.send(embed=dev_embed)


class IdeaModal(Modal):
    
    def __init__(self, locale: dict, bot: disnake.ext.commands.bot.InteractionBot, interaction: disnake.AppCmdInter) -> None:
        self.locale = locale
        self.bot = bot
        self.interaction = interaction
        components = [
            TextInput(
                label=f"{locale['textinput_label_1']}",
                placeholder=f"{locale['textinput_placeholder_1']}",
                custom_id="description",
                style=TextInputStyle.paragraph
            ),
            TextInput(
                label=f"{locale['textinput_label_2']}",
                placeholder=f"{locale['textinput_placeholder_2']}",
                custom_id="image",
                style=TextInputStyle.short,
                required=False
            )
        ]

        super().__init__(title=f"{locale['modal_title']}", 
                         components=components,
                         custom_id="report_modal",
                         timeout=300)

    async def callback(self, inter: ModalInteraction) -> None:

        dev_embed = disnake.Embed(
            title="Новая идея!",
            description=f"Пришла новая идея с сервера `{self.interaction.guild.name}`"
        ).add_field(
            name="Придумал:",
            value=f"{self.interaction.author.mention}\n`{self.interaction.author}`"
        ).add_field(
            name="Описание идеи:",
            value=inter.text_values["description"]
        )
        
        user_embed = disnake.Embed(
            title=self.locale["embed_title"],
            description=self.locale["embed_descriprion"]
        )

        if inter.text_values["image"] and "https://" in inter.text_values["image"]:
            dev_embed.add_field(
                name="Пример",
                value=f"[Клик...]({inter.text_values['image']})"
            )

        await inter.response.send_message(embed=user_embed, ephemeral=True, view=SupportButton())
        await self.bot.idea_channel.send(embed=dev_embed)