import disnake
from disnake import MessageInteraction, ModalInteraction
from disnake.ui import Modal, TextInput

from core.models.profiles import Profiles
from tools.ui.components import StandartButton, StandartView, BackButton
from tools.ui.admin_panel.modals import RatingModal

units = ["seconds", "minutes", "hours", "days", "weeks"]


def return_time(duration: int, unit: str):
    units_ = {
        "seconds" or "секунд": duration,
        "minutes" or "минут": duration * 60,
        "hours" or "часов": duration * 3600,
        "days" or "дней": duration * 86400,
        "weeks" or "недель": duration * 604800
    }
    return units_[unit]


class MuteModal(Modal):

    def __init__(self, member: disnake.Member, unit: str, locale: dict, embed: disnake.Embed, view_: StandartView, view_time: StandartView):
        components = [
            TextInput(
                label=locale[f"{unit}"],
                style=disnake.TextInputStyle.single_line,
                placeholder=locale[f"mute_modal_ph"],
                required=True,
                custom_id=unit
            )
        ]
        super().__init__(timeout=30, components=components, title=locale["mute_title"])
        self.member: disnake.Member = member
        self.locale: dict = locale
        self.embed: disnake.Embed = embed
        self.unit = unit
        self.view_ = view_
        self.view_time = view_time

    async def callback(self, interaction: ModalInteraction) -> None:
        await self.member.timeout(duration=return_time(int(interaction.text_values[self.unit]), unit=self.unit))
        self.view_.children[2] = MuteButtons(self.member, self.locale, self.embed, "unmute")
        embed = self.embed.copy()
        embed.title = self.locale["mute_title"]
        embed.description = self.locale["mute_description_modal"].format(time=f"{interaction.text_values[self.unit]} {self.locale[self.unit]}")
        new_view = StandartView(self.view_.inter, self.view_.client, 30)
        new_view.add_item(BackButton(self.embed, self.view_.children, self.locale))
        new_view.flag = 1
        await interaction.response.edit_message(embed=embed, view=new_view)


class BanButton(StandartButton):

    def __init__(self, member: disnake.Member, locale, embed: disnake.Embed):
        super().__init__(label=locale['ban'], emoji="<:BanHammer:1201595375228825651>", style=disnake.ButtonStyle.blurple,
                         row=1)
        self.member: disnake.Member = member
        self.locale: dict = locale
        self.embed: disnake.Embed = embed

    async def callback(self, interaction: MessageInteraction, /) -> None:
        if self.member.top_role >= interaction.me.top_role:
            return await interaction.response.send_message(self.locale["error_ban"], ephemeral=True)

        self.view.flag = 1
        await self.member.ban()
        self.embed.description = self.locale['ban_description'].format(member=self.member.mention)
        await interaction.response.edit_message(embed=self.embed, view=None)


class TimesTypesButtons(StandartButton):

    def __init__(self, member: disnake.Member, unit: str, locale: dict, embed: disnake.Embed, view_: StandartView):
        super().__init__(label=locale[unit], style=disnake.ButtonStyle.red, row=1)
        self.member: disnake.Member = member
        self.locale: dict = locale
        self.embed: disnake.Embed = embed
        self.unit = unit
        self.view_ = view_

    async def callback(self, interaction: MessageInteraction) -> None:
        self.view.flag = 1
        await interaction.response.send_modal(MuteModal(self.member, self.unit, self.locale, self.embed, self.view_, self.view))


class MuteButtons(StandartButton):

    def __init__(self, member: disnake.Member, locale, embed: disnake.Embed, type_: str):
        super().__init__(label=locale[type_],
                         emoji=locale[f"{type_}_emoji"],
                         style=disnake.ButtonStyle.blurple,
                         row=1)
        self.member: disnake.Member = member
        self.locale: dict = locale
        self.embed: disnake.Embed = embed
        self.type_ = type_

    async def callback(self, interaction: MessageInteraction, /) -> None:
        if self.member.top_role >= interaction.me.top_role:
            await interaction.response.send_message(self.locale[f"error_{self.type_}"], ephemeral=True)

        self.view.flag = 1
        embed = self.embed.copy()

        if self.type_ == "mute":
            new_view = StandartView(self.view.inter, self.view.client, 30)
            embed.title = self.locale["mute_title"]
            embed.description = self.locale["mute_description"]

            for i in range(5):
                new_view.add_item(TimesTypesButtons(self.member, units[i], self.locale, self.embed, self.view))
            new_view.add_item(BackButton(self.embed, self.view.children, self.locale))
            return await interaction.response.edit_message(embed=embed,
                                                           view=new_view)
        if self.type_ == "unmute":
            new_view = StandartView(self.view.inter, self.view.client, 30)
            self.view.children[2] = MuteButtons(self.member, self.locale, self.embed, "mute")
            embed.title = self.locale["unmute_title"]
            embed.description = self.locale["unmute_description"]
            await self.member.timeout(duration=0)
            new_view.add_item(BackButton(self.embed, self.view.children, self.locale))
            return await interaction.response.edit_message(embed=embed, view=new_view)


class KickButton(StandartButton):

    def __init__(self, member: disnake.Member, locale, embed: disnake.Embed):
        super().__init__(label=locale['kick'], emoji="<:kick:1201595459337195571>", style=disnake.ButtonStyle.blurple,
                         row=1)
        self.member: disnake.Member = member
        self.locale: dict = locale
        self.embed: disnake.Embed = embed

    async def callback(self, interaction: MessageInteraction, /) -> None:
        if self.member.top_role >= interaction.me.top_role:
            return await interaction.response.send_message(self.locale["error_kick"], ephemeral=True)

        self.view.flag = 1
        await self.member.kick()
        self.embed.description = self.locale['kick_description'].format(member=self.member.mention)
        await interaction.response.edit_message(embed=self.embed, view=None)


async def get_rating_item(member: Profiles, item: str) -> int:
    if item == "level":
        return member.level
    elif item == "money":
        return member.money
    elif item == "messages":
        return member.messages
    elif item == "experience":
        return member.experience


class AddAndRemoveButtons(StandartButton):

    def __init__(self,
                 emoji: str,
                 type_of_rating: str,
                 type_of_action: str,
                 member: disnake.Member,
                 member_profile: Profiles,
                 embed: disnake.Embed,
                 locale: dict,
                 style: disnake.ButtonStyle
                 ):
        self.locale: dict = locale
        self.type_of_rating: str = type_of_rating
        self.member: disnake.Member = member
        self.type_of_action: str = type_of_action
        self.member_profile: Profiles = member_profile
        self.embed: disnake.Embed = embed
        super().__init__(emoji=emoji, label=locale[f"{type_of_action}"], row=1, style=style)

    async def callback(self, interaction: disnake.MessageInteraction, /) -> None:
        await interaction.response.send_modal(RatingModal(self.type_of_rating, self.type_of_action, self.member,
                                                          self.member_profile, self.embed, self.locale, self.view))


class StubButton(StandartButton):

    def __init__(self, label: str, emoji: str, style: disnake.ButtonStyle, row: int, locale: dict, type_: str):
        super().__init__(disabled=False, label=locale[label], emoji=emoji, style=style, row=row)
        self.locale = locale
        self.type_ = type_

    async def callback(self, interaction: MessageInteraction, /) -> None:
        await interaction.response.send_message(self.locale[self.type_], ephemeral=True)


class RatingPanelButtons(StandartButton):

    def __init__(self,
                 emoji: str,
                 type_of_rating: str,
                 member: disnake.Member,
                 member_profile: Profiles,
                 embed: disnake.Embed,
                 locale: dict,
                 ):
        self.locale: dict = locale
        self.member: disnake.Member = member
        self.type_of_rating: str = type_of_rating
        self.member_profile: Profiles = member_profile
        self.embed: disnake.Embed = embed
        super().__init__(emoji=emoji, label=locale[f"{type_of_rating}"], row=2, style=disnake.ButtonStyle.blurple)

    async def callback(self, interaction: disnake.MessageInteraction) -> None:
        self.view.flag = 1
        new_view = StandartView(self.view.inter, self.view.client, 30)
        new_view.add_item(AddAndRemoveButtons("<:remove_red:1201473198038994944>", self.type_of_rating, "remove",
                                              self.member, self.member_profile, self.embed,
                                              self.locale, disnake.ButtonStyle.red))
        new_view.add_item(AddAndRemoveButtons("<:download_emojigg:1201474077517430834>", self.type_of_rating, "set",
                                              self.member, self.member_profile, self.embed,
                                              self.locale, disnake.ButtonStyle.blurple))
        new_view.add_item(AddAndRemoveButtons("<:add_green:1201473107991470201>", self.type_of_rating, "add",
                                              self.member, self.member_profile, self.embed,
                                              self.locale, disnake.ButtonStyle.green))
        new_view.add_item(BackButton(self.embed, self.view.children, self.locale))
        await interaction.response.edit_message(embed=disnake.Embed(title=f"{self.locale['change'].format(type=self.locale[f'{self.type_of_rating}_edit'])}",
                                                                    description=self.locale['take_action'])
                                                .add_field(name=self.locale[self.type_of_rating],
                                                           value=await get_rating_item(self.member_profile,
                                                                                       self.type_of_rating)),
                                                view=new_view)
