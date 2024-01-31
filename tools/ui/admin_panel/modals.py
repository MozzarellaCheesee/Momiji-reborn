import disnake
from disnake import ModalInteraction
from disnake.ui import Modal, TextInput

from core.models.profiles import Profiles
from tools.ui.components import StandartView


def return_time(duration: int, unit: str):
    units_ = {
        "seconds" or "секунд": duration,
        "minutes" or "минут": duration * 60,
        "hours" or "часов": duration * 3600,
        "days" or "дней": duration * 86400,
        "weeks" or "недель": duration * 604800
    }
    return units_[unit]


async def change_rating(member_profile: Profiles, type_of_rating: str, type_of_action: str, quantity: int) -> Profiles:
    if type_of_action == "set":
        if type_of_rating == "level":
            member_profile.level = quantity
        elif type_of_rating == "messages":
            member_profile.messages = quantity
        elif type_of_rating == "experience":
            member_profile.experience = quantity
        elif type_of_rating == "money":
            member_profile.money = quantity
        await member_profile.save()
        return member_profile

    change = {
        "remove": -int(quantity),
        "add": int(quantity)
    }

    if type_of_rating == "level":
        member_profile.level += change[type_of_action]
    elif type_of_rating == "messages":
        member_profile.messages += change[type_of_action]
    elif type_of_rating == "experience":
        member_profile.experience += change[type_of_action]
    elif type_of_rating == "money":
        member_profile.money += change[type_of_action]
    await member_profile.save()
    return member_profile


class MuteModal(Modal):

    def __init__(self, member: disnake.Member, unit: str, locale: dict, embed: disnake.Embed, view_: StandartView):
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

    async def callback(self, interaction: ModalInteraction) -> None:
        await self.member.timeout(duration=return_time(int(interaction.text_values[self.unit]), unit=self.unit))
        self.view_.children[2].change_type("unmute")
        new_view = StandartView(self.view_.inter, self.view_.client, 30)
        embed = self.embed.copy()
        embed.title = self.locale["mute_title"]
        embed.description = self.locale["mute_description_modal"].format(time=f"{interaction.text_values[self.unit]} {self.locale[self.unit]}")
        await interaction.response.edit_message(embed=embed)


class RatingModal(Modal):

    def __init__(self,
                 type_of_rating: str,
                 type_of_action: str,
                 member: disnake.Member,
                 member_profile: Profiles,
                 embed: disnake.Embed,
                 locale: dict,
                 view: StandartView):
        self.member = member
        self.member_profile = member_profile
        self.type_of_action = type_of_action
        self.type_of_rating = type_of_rating
        self.embed = embed
        self.locale = locale
        self.view_ = view
        components = [
            TextInput(
                label=locale[f"{type_of_rating}_modal_component"],
                style=disnake.TextInputStyle.single_line,
                placeholder=locale[f"{type_of_rating}_modal_ph"],
                required=True,
                custom_id=type_of_rating
            )
        ]
        super().__init__(title=locale[f"{type_of_rating}"], components=components, timeout=40)

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        try:
            self.member_profile = await change_rating(self.member_profile, self.type_of_rating,
                                                      self.type_of_action, interaction.text_values[self.type_of_rating])
            self.view_.member_profile = self.member_profile
            embed = self.embed.copy()
            embed.title = f"{self.locale['change'].format(type=self.locale[f'{self.type_of_rating}_edit'])}"
            embed.description = self.locale["changed_modal"].format(type=self.locale[f'{self.type_of_rating}_modal_component'])
            self.embed.description = self.locale["description"].format(member=self.member.mention,
                                                                       money=self.member_profile.money,
                                                                       level=self.member_profile.level,
                                                                       messages=self.member_profile.messages,
                                                                       experience=self.member_profile.experience,
                                                                       warns=len(await self.member_profile.warns),
                                                                       tickets=len(await self.member_profile.tickets))
            await interaction.response.edit_message(embed=embed, view=self.view_)
        except ValueError:
            await interaction.response.edit_message(embed=disnake.Embed(title=self.locale['error_title'],
                                                                        description=self.locale['error_desc']))
