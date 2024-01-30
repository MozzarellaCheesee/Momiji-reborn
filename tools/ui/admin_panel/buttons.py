import disnake
from disnake import MessageInteraction
from disnake.errors import Forbidden

from core.models.profiles import Profiles
from tools.ui.components import StandartButton, StandartView, BackButton
from tools.ui.admin_panel.modals import RatingModal


class BanButton(StandartButton):

    def __init__(self, member: disnake.Member, locale, embed: disnake.Embed):
        super().__init__(label=locale['ban'], emoji="<:BanHammer:1201595375228825651>", style=disnake.ButtonStyle.blurple,
                         row=1)
        self.member: disnake.Member = member
        self.locale: dict = locale
        self.embed: disnake.Embed = embed

    async def callback(self, interaction: MessageInteraction, /) -> None:
        if self.member.top_role >= interaction.me.top_role:
            await interaction.response.send_message(self.locale["error_ban"], ephemeral=True)
        self.view.flag = 1
        await self.member.ban()
        self.embed.description = self.locale['ban_description'].format(member=self.member.mention)
        await interaction.response.edit_message(embed=self.embed, view=None)


class MuteButtons(StandartButton):

    def __init__(self):
        ...


class KickButton(StandartButton):

    def __init__(self, member: disnake.Member, locale, embed: disnake.Embed):
        super().__init__(label=locale['kick'], emoji="<:kick:1201595459337195571>", style=disnake.ButtonStyle.blurple,
                         row=1)
        self.member: disnake.Member = member
        self.locale: dict = locale
        self.embed: disnake.Embed = embed

    async def callback(self, interaction: MessageInteraction, /) -> None:
        if self.member.top_role >= interaction.me.top_role:
            await interaction.response.send_message(self.locale["error_kick"], ephemeral=True)
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

    def __init__(self, label: str, emoji: str, style: disnake.ButtonStyle, row: int, locale: dict, type_: str,
                 disabled: bool = False):
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
