import disnake
from disnake.ui import Modal, TextInput, View, Button
from disnake.ext import commands
from disnake import TextInputStyle, ModalInteraction, MessageInteraction


from tortoise.exceptions import DoesNotExist
from random import randint
from asyncio import sleep
import validators
import re



class VerefyModal(Modal):

    def __init__(self, client, code, role, locale) -> None:
        components = [
            TextInput(
                label=locale["setup_modal"]["components"]["labels"]["verefy"],
                style=TextInputStyle.single_line,
                placeholder=code,
                required=False,
                custom_id="verefy"
            )
        ]
        super().__init__(title=locale["setup_modal"]["titles"]["verefy"], components=components, timeout=600)
        self.client: commands.InteractionBot = client
        self.locale = locale
        self.role = role
        self.code = code

    async def callback(self, inter: ModalInteraction) -> None:
        if str(self.code) != inter.text_values["verefy"]:
            return await inter.response.send_message(self.locale["not_verefy"], ephemeral=True)

        member: disnake.Member = inter.guild.get_member(inter.author.id)

        if member.top_role >= inter.me.top_role:
            return await inter.response.send_message(self.locale["top_role_error"], ephemeral=True)

        await inter.response.send_message(
            embed=disnake.Embed(
                description=self.locale["verefy"]["description"]
            ), ephemeral=True
        )
        await sleep(5)
        


        await member.add_roles(self.role, reason='verify')


class VerefyButton(View):

    def __init__(self, client, locale):
        super().__init__(timeout=None)
        self.client = client
        self.locale = locale

    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="<:momiji_verefy:1128318165542248538>", custom_id="verefy")
    async def a_callback(self, button, interaction: MessageInteraction):
        locale = self.locale(interaction.locale, "verefy")
        defaults = {
            "discord_id": interaction.guild.id
        }
        server = await self.client.db.Servers.get_or_create(defaults=defaults, discord_id=interaction.guild.id)
        try:
            role = await self.client.db.Roles.get(server=server[0], role_type="VERIFY")
            role_in_discord: disnake.Role = interaction.guild.get_role(role.role_id)
            code = randint(1000, 9999)
            await interaction.response.send_modal(VerefyModal(self.client, code, role_in_discord, locale))
        except DoesNotExist:
            await interaction.response.send_message(
                embed=disnake.Embed(
                    description=locale["not_role"]
                ),
                ephemeral=True)

class VerefySetupModal(Modal):

    def __init__(self, locale, lang_locale, client, channel) -> None:
        components: list = [
            TextInput(
                label=locale["setup_modal"]["components"]["labels"]["color"],
                style=TextInputStyle.single_line,
                placeholder=locale["setup_modal"]["components"]["placeholders"]["color"],
                required=False,
                custom_id="color"
            ),
            TextInput(
                label=locale["setup_modal"]["components"]["labels"]["title"],
                style=TextInputStyle.single_line,
                placeholder=locale["setup_modal"]["components"]["placeholders"]["title"],
                required=False,
                custom_id="title"
            ),
            TextInput(
                label=locale["setup_modal"]["components"]["labels"]["description"],
                style=TextInputStyle.paragraph,
                placeholder=locale["setup_modal"]["components"]["placeholders"]["description"],
                required=False,
                custom_id="description"
            ),
            TextInput(
                label=locale["setup_modal"]["components"]["labels"]["image"],
                style=TextInputStyle.single_line,
                placeholder=locale["setup_modal"]["components"]["placeholders"]["image"],
                required=False,
                custom_id="image"
            ),
            TextInput(
                label=locale["setup_modal"]["components"]["labels"]["footer"],
                style=TextInputStyle.single_line,
                placeholder=locale["setup_modal"]["components"]["placeholders"]["footer"],
                required=False,
                custom_id="footer"
            )
        ]
        super().__init__(title=locale["setup_modal"]["titles"]["modal"], timeout=600, components=components)
        self.client = client
        self.locale = locale
        self.channel: disnake.TextChannel = channel
        self.lang_locale = lang_locale
    
    async def callback(self, inter: ModalInteraction) -> None:

        color = 0x2b2d31

        embed_components = {}

        if re.fullmatch(r'[A-Fa-f0-9]{6}', inter.text_values["color"]):
            color = int(inter.text_values["color"], 16)

        if inter.text_values["title"]:
            embed_components["title"] = inter.text_values["title"]
        if inter.text_values["description"]:
            embed_components["description"] = inter.text_values["description"]
        if inter.text_values["image"] and validators.url(inter.text_values["image"]):
            embed_components["image"] = inter.text_values["image"]

        if len(embed_components) < 1: 
            return await inter.response.send_message(self.locale["item_error"], ephemeral=True)

        embed = disnake.Embed(color = color)

        try:
            embed.title=embed_components["title"]
        except:
            ...

        try:
            embed.description=embed_components["description"]
        except:
            ...

        try:
            embed.set_image(url=embed_components["image"])
        except:
            ...
        
        try:
            embed.set_footer(text=inter.text_values["footer"])
        except:
            ...

        

        await inter.response.send_message(
            embed=disnake.Embed(
                description=self.locale["setup_modal"]["embeds"]["title"]
            ), ephemeral=True
        )

        await self.channel.send(
            embed=embed, view=VerefyButton(self.client, self.lang_locale)
        )