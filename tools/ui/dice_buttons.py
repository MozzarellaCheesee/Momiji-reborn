import disnake

from random import randint
from asyncio import sleep

from tools.ui.components import StandartButton

sides = ["https://cdn.discordapp.com/attachments/1123682099233300602/1200735127643373619/1.gif?ex=65c742bb&is=65b4cdbb&"
         "hm=ff225ff624f582b833c75ab5423e5824ccd0afd292d2bdd0ea6a3fb4a26f1aea&",
         "https://cdn.discordapp.com/attachments/1123682099233300602/1200735128155070474/2.gif?ex=65c742bb&is=65b4cdbb&"
         "hm=a2f27e07ec36f61e514dd361b732032fff09c1e71a761ca953c4c339cb263ce3&",
         "https://cdn.discordapp.com/attachments/1123682099233300602/1200735128918442014/3.gif?ex=65c742bb&is=65b4cdbb&"
         "hm=cef2573722c54720a5844de05f5fea3fc7daddf39629524e357b957229e3a54f&",
         "https://cdn.discordapp.com/attachments/1123682099233300602/1200735129279144036/4.gif?ex=65c742bb&is=65b4cdbb&"
         "hm=781ea110edd81162fec8c763edd40b788af8bba895077ca25353288811dc6dad&",
         "https://cdn.discordapp.com/attachments/1123682099233300602/1200735129727938662/5.gif?ex=65c742bb&is=65b4cdbb&"
         "hm=b6742d695f61fe1201a89a3857ac35b77786f174c6d32ed249948b3afc8ecae6&",
         "https://cdn.discordapp.com/attachments/1123682099233300602/1200735126536077322/6.gif?ex=65c742ba&is=65b4cdba&"
         "hm=17381dbfd1c2a8e6c55d120e25856287622199355a2c682ddef0ce4aa7d0ed17&"]

multipy = {"1": 6, "2": 3, "3": 2}


class PlayButton(StandartButton):

    def __init__(self, locale: dict, bet: int):
        self.locale = locale
        self.bet = bet
        super().__init__(label=locale["play_btn"], style=disnake.ButtonStyle.green, row=1,
                         emoji="<:play:1200744974497632256>")

    async def callback(self, interaction: disnake.Interaction) -> None:
        side = randint(1, 6)
        await interaction.response.edit_message(embed=disnake.Embed(title=self.locale["throw"])
                                                .set_image(url=sides[side - 1]), view=None)

        await sleep(4)
        self.view.timeout = None

        if side in self.view.list_num:
            self.view.author_profile.money += self.bet * multipy[f'{len(self.view.list_num)}']
            await self.view.author_profile.save()
            await self.view.inter.edit_original_message(embed=disnake.Embed(
                title=self.locale["title"].format(member=self.view.inter.author.name),
                description=f"{self.locale['win']} "
                            f"{self.bet * multipy[f'{len(self.view.list_num)}']} "
                            f"<a:momiji_crystal:1126456975337730078>")
                            .set_footer(text=self.locale["result"].format(side=side)), view=None
            )
        else:
            self.view.author_profile.money -= self.bet
            await self.view.author_profile.save()
            await self.view.inter.edit_original_message(embed=disnake.Embed(
                title=self.locale["title"].format(member=self.view.inter.author.name),
                description=f"{self.locale['lose']} "
                            f"{self.bet} <a:momiji_crystal:1126456975337730078>")
                            .set_footer(text=self.locale["result"].format(side=side)), view=None
            )


class BackButton(StandartButton):

    def __init__(self, locale: dict):
        super().__init__(label=locale["back_btn"], style=disnake.ButtonStyle.red, row=2,
                         emoji="<:back:1200744962334142626>")

    async def callback(self, interaction: disnake.Interaction) -> None:
        await self.view.inter.delete_original_message()


class DiceButtons(StandartButton):

    def __init__(self, emoji: str, row: int, num: int, locale: dict):
        self.num = num
        self.locale = locale
        super().__init__(emoji=emoji, style=disnake.ButtonStyle.grey, row=row)

    async def callback(self, interaction: disnake.Interaction) -> None:

        if self.num in self.view.list_num:
            self.style = disnake.ButtonStyle.grey
            self.view.list_num.remove(self.num)
            await interaction.response.edit_message(view=self.view)
        else:
            if len(self.view.list_num) == 3:
                return await interaction.response.send_message(
                    embed=disnake.Embed(title=self.locale["title"]
                                        .format(member=self.view.inter.author.name),
                                        description=self.locale["error_count"]),
                    ephemeral=True)
            self.style = disnake.ButtonStyle.blurple
            self.view.list_num.append(self.num)
            await interaction.response.edit_message(view=self.view)
