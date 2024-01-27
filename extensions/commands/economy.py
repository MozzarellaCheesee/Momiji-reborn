import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from random import randint, getrandbits
from asyncio import sleep

from core.cog import BaseCog
from core.checks import BaseChecks
from core.i18n import LocalizationStorage
from tools.exeption import CustomError
from tools.ui.components import StandartView
from tools.ui.dice_buttons import DiceButtons, BackButton, PlayButton

_ = LocalizationStorage("economy")
err = LocalizationStorage("errors#2")

COIN_SIDES = ["head", "tail"]
CUBE_SIDES = ["<:dice_1:1200716726791307335>", "<:dice_2:1200716728691343490>",
              "<:dice_3:1200716731707039797>", "<:dice_4:1200716735091843142>",
              "<:dice_5:1200716736987664485>", "<:dice_6:1200716739692994602>"]


class Economy(BaseCog):

    @commands.slash_command(name=__("economy", key="COMMAND_GROUP_ECONOMY"),
                            description=__("economy commands", key="COMMAND_GROUP_DESCRIPTION_ECONOMY"))
    async def economy(self, inter: AppCmdInter):
        ...

    @commands.cooldown(1, 28800, commands.BucketType.user)
    @economy.sub_command(name=__("work", key="COMMAND_NAME_WORK"),
                         description=__("get money and experience", key="COMMAND_DESCRIPTION_WORK"))
    async def work(self, inter: AppCmdInter):
        locale = _(inter.locale, "work")
        true_or_false = getrandbits(1)
        money = randint(50, 150)
        experience = randint(16, 45)

        user_in_db = await self.client.db.Users.get_or_create(discord_id=inter.author.id)
        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.author.guild.id)
        profile = await self.client.db.Profiles.get_or_none(user=user_in_db[0], server=server_in_db[0])

        if not profile:
            return await inter.send(locale['error'], ephemeral=True)

        profile.money = profile.money + money

        embed = disnake.Embed(title=locale["title"], description=locale["description"]) \
            .add_field(name=locale["field_name_1"], value=f'> `{money}` <a:momiji_crystal:1126456975337730078>') \
            .set_thumbnail(url=inter.author.display_avatar.url)
        if true_or_false == 1:
            profile.experience = profile.experience + experience
            embed.add_field(name=locale["field_name_2"],
                            value=f'> `{experience}` <a:momiji_experience:1126492132086136892>')

        await profile.save()
        await inter.send(embed=embed)

    @BaseChecks.self_check(err)
    @economy.sub_command(name=__("pay", key="COMMAND_NAME_PAY"),
                         description=__("transfer money to a user", key="COMMAND_DESCRIPTION_PAY"))
    async def pay(self, inter: AppCmdInter,
                  member: disnake.User = commands.Param(name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                                                        description=__("select member",
                                                                       key="COMMAND_PARAM_DESCRIPTION_MEMBER")),
                  amount: int = commands.Param(name=__("amount", key="COMMAND_PARAM_NAME_AMOUNT"),
                                               description=__("enter amount", key="COMMAND_PARAM_DESCRIPTION_AMOUNT"))
                  ):
        locale = _(inter.locale, "pay")
        if member.bot:
            raise CustomError(locale["error_bot"])

        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.author.guild.id)
        author_user_in_db = await self.client.db.Users.get_or_create(discord_id=inter.author.id)
        author_profile = await self.client.db.Profiles.get_or_none(user=author_user_in_db[0], server=server_in_db[0])

        if author_profile is None:
            return await inter.send(locale['error_'], ephemeral=True)

        if author_profile.money < amount:
            raise CustomError(locale["error"])

        member_user_in_db = await self.client.db.Users.get_or_create(discord_id=member.id)
        member_profile = await self.client.db.Profiles.get_or_none(user=member_user_in_db[0], server=server_in_db[0])

        if member_profile is None:
            return await inter.send(locale['error__'], ephemeral=True)

        member_profile.money += amount
        author_profile.money -= amount
        await member_profile.save()
        await author_profile.save()

        await inter.send(embed=disnake.Embed(title=locale["title"], description=locale["description"])
                         .add_field(name=locale["field_name_1"],
                                    value=f'> `{amount}` <a:momiji_crystal:1126456975337730078>')
                         .set_thumbnail(url=inter.author.display_avatar.url))

    @economy.sub_command(name=__("russian-roulette", key="COMMAND_NAME_ROULETTE"),
                         description=__("play with dead", key="COMMAND_DESCRIPTION_ROULETTE"))
    async def rus_roulette(self, inter: AppCmdInter,
                           bullets: int = commands.Param(name=__("bullets", key="bullets"),
                                                         description=__("enter bullets count", key="bullets_desc"),
                                                         le=5,
                                                         ge=1),
                           amount: int = commands.Param(name=__("bet", key="money"),
                                                        description=__("enter stake", key="money_desc"),
                                                        ge=50, le=1000000)):
        locale = _(inter.locale, "roulette")
        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.author.guild.id)
        author_user_in_db = await self.client.db.Users.get_or_create(discord_id=inter.author.id)
        author_profile = await self.client.db.Profiles.get_or_none(user=author_user_in_db[0], server=server_in_db[0])

        if author_profile is None:
            return await inter.send(locale['error_'], ephemeral=True)

        if author_profile.money < amount:
            raise CustomError(locale["error"])

        drum = set()
        while len(drum) != bullets:
            num = randint(1, 6)
            drum.add(num)
        bull = randint(1, 6)

        if bull in drum:
            author_profile.money -= amount
            await author_profile.save()
            await inter.send(embed=disnake.Embed(title=locale["dead_title"], description=locale["dead_description"])
                             .add_field(name=locale["summ_lose"], value=f"{amount} <a:momiji_crystal:112645697"
                                                                        f"5337730078>")
                             .add_field(name=locale["balance"], value=f"{author_profile.money} <a:momiji_crystal:"
                                                                      f"1126456975337730078>")
                             .set_thumbnail(url=inter.author.display_avatar))
        else:
            author_profile.money += amount * (bullets + 1) - amount
            await author_profile.save()
            await inter.send(embed=disnake.Embed(title=locale["win_title"], description=locale["win_description"])
                             .add_field(name=locale["summ_win"], value=f"{amount * (bullets + 1) - amount} <a:momiji_"
                                                                       f"crystal:1126456975337730078>")
                             .add_field(name=locale["balance"], value=f"{author_profile.money} <a:momiji_crystal:"
                                                                      f"1126456975337730078>")
                             .set_thumbnail(url=inter.author.display_avatar))

    @economy.sub_command(name=__("coinflip", key="COMMAND_NAME_COINFLIP"),
                         description=__("flip a coin", key="COMMAND_DESCRIPTION_COINFLIP"))
    async def coinflip(self, inter: AppCmdInter,
                       side: str = commands.Param(name=__("side", key="side"), description=__("choose a side",
                                                                                              key="side_desc"),
                                                  choices=[__("head", key="heads"), __("tail", key="tail")]),
                       amount: int = commands.Param(name=__("bet", key="COMMAND_PARAM_NAME_AMOUNT"),
                                                    description=__("enter amount",
                                                                   key="COMMAND_PARAM_DESCRIPTION_AMOUNT"),
                                                    ge=50, le=1000000)):
        locale = _(inter.locale, "coinflip")
        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.author.guild.id)
        author_user_in_db = await self.client.db.Users.get_or_create(discord_id=inter.author.id)
        author_profile = await self.client.db.Profiles.get_or_none(user=author_user_in_db[0], server=server_in_db[0])
        result = getrandbits(1)

        if author_profile is None:
            return await inter.send(locale['error_'], ephemeral=True)

        if author_profile.money < amount:
            raise CustomError(locale["error"])

        await inter.send(embed=disnake.Embed(title=locale["wait_title"])
                         .set_image(url="https://usagif.com/wp-content/"
                                        "uploads/gifs/coin-flip-11.gif"))
        await sleep(5)

        if COIN_SIDES[result] == side:
            author_profile.money += amount * 2
            await author_profile.save()
            await inter.edit_original_message(embed=disnake.Embed(title=locale["win_title"],
                                                                  description=locale["win_description"])
                                              .add_field(name=locale["summ_win"], value=f"{amount * 2 - amount} "
                                                                                        f"<a:momiji_crystal:"
                                                                                        f"1126456975337730078>")
                                              .add_field(name=locale["balance"], value=f"{author_profile.money}<a:momij"
                                                                                       f"i_crystal:112645697533773007"
                                                                                       f"8>")
                                              .set_thumbnail(url="https://cdn.discordapp.com/attachments/85281641389031"
                                                             "4251/1200533089718382612/Cz9V8qDRyTE.jpg?ex=65c68691&is=6"
                                                             "5b41191&hm=7d013964aba8ed2b82b070903d67741f72619493f8219c"
                                                             "f559aa8bc633dd0c28&"))
        else:
            author_profile.money += amount
            await author_profile.save()
            await inter.edit_original_message(embed=disnake.Embed(title=locale["lose_title"],
                                                                  description=locale["lose_description"])
                                              .add_field(name=locale["summ_lose"], value=f"{amount} <a:momiji_crystal"
                                                                                         f":1126456975337730078>")
                                              .add_field(name=locale["balance"], value=f"{author_profile.money}<a:momij"
                                                                                       f"i_crystal:112645697533773007"
                                                                                       f"8>")
                                              .set_thumbnail(url="https://cdn.discordapp.com/attachments/85281641389031"
                                                             "4251/1200533089479311493/Eq_X5Bbm5Jc.jpg?ex=65c68691&is=6"
                                                             "5b41191&hm=bb696bd5e7bcaa76eea8718893ab6f5f5c1345e8c386dd"
                                                             "f3fbf8806828852952&"))

    @commands.cooldown(1, 20, commands.BucketType.user)
    @economy.sub_command(name=__("dice", key="COMMAND_NAME_DICE"),
                         description=__("throw the dice", key="COMMAND_DESCRIPTION_DICE"))
    async def dice(self, inter: AppCmdInter,
                   bet: int = commands.Param(name=__("bet", key="COMMAND_PARAM_NAME_AMOUNT"),
                                             description=__("enter amount", key="COMMAND_PARAM_DESCRIPTION_AMOUNT"),
                                             ge=50, le=1000000)):
        locale = _(inter.locale, "dice")
        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.author.guild.id)
        author_user_in_db = await self.client.db.Users.get_or_create(discord_id=inter.author.id)
        author_profile = await self.client.db.Profiles.get_or_none(user=author_user_in_db[0], server=server_in_db[0])

        if author_profile is None:
            return await inter.send(locale['error_'], ephemeral=True)

        if author_profile.money < bet:
            raise CustomError(locale["error"])

        Btn_view = StandartView(inter, self.client, timeout=20)
        Btn_view.list_num = []
        Btn_view.author_profile = author_profile

        con = 0
        for i in range(6):
            if con < 3:
                row = 1
            else:
                row = 2
            Btn_view.add_item(DiceButtons(CUBE_SIDES[i], row=row, num=i+1, locale=locale))
            con += 1
        Btn_view.add_item(PlayButton(locale, bet))
        Btn_view.add_item(BackButton(locale))

        await inter.send(embed=disnake.Embed(title=locale["title"].format(member=inter.author.name),
                                             description=locale["description"])
                         .set_image(url="https://cdn.discordapp.com/attachments/"
                                        "1123682099233300602/1200735127165218856"
                                        "/inf.gif?ex=65c742ba&is=65b4cdba&hm=b37"
                                        "30f0860f5ac1038bd11942805db6dd7b24bb681c55299c2a50932adae11ad&"),
                         view=Btn_view)


def setup(client: commands.InteractionBot):
    client.add_cog(Economy(client))
