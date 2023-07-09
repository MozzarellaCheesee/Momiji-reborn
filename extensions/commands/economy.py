import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from random import randint, getrandbits

from core.cog import BaseCog
from core.checks import BaseChecks
from core.i18n import LocalizationStorage
from tools.utils import get_member_profile
from tools.exeption import CustomError

_ = LocalizationStorage("economy")
err = LocalizationStorage("errors#2")

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

        profile = await get_member_profile(inter.author, self.client)
        profile.money = profile.money + money

        embed = disnake.Embed(
            title=locale["title"],
            description=locale["description"]
        ).add_field(
            name=locale["field_name_1"],
            value=f'> `{money}` <a:momiji_crystal:1126456975337730078>'
        ).set_thumbnail(
            url=inter.author.display_avatar.url
        )

        if true_or_false == 1:
            profile.experience = profile.experience + experience
            embed.add_field(
                name=locale["field_name_2"],
                value=f'> `{experience}` <a:momiji_experience:1126492132086136892>'
            )

        await profile.save()
        await inter.send(embed=embed)
 
    @BaseChecks.self_check(err)
    @economy.sub_command(name=__("pay", key="COMMAND_NAME_PAY"),
                         description=__("transfer money to a user", key="COMMAND_DESCRIPTION_PAY"))
    async def pay(
        self, 
        inter: AppCmdInter,
        member: disnake.User = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER")
        ),
        amount: int = commands.Param(
            name=__("amount", key="COMMAND_PARAM_NAME_AMOUNT"),
            description=__("enteramount", key="COMMAND_PARAM_DESCRIPTION_AMOUNT")
        )
    ):
        locale = _(inter.locale, "pay")
        if member.bot:
            raise CustomError(locale["error_bot"])

        author_profile = await get_member_profile(inter.author, self.client)

        if author_profile.money < amount:
            raise CustomError(locale["error"])
        
        member_profile = await get_member_profile(member, self.client)

        member_profile.money = member_profile.money + amount
        author_profile.money = author_profile.money - amount
        await member_profile.save()
        await author_profile.save()

        await inter.send(
            embed=disnake.Embed(
                title=locale["title"],
                description=locale["description"]
            ).add_field(
                name=locale["field_name_1"],
                value=f'> `{amount}` <a:momiji_crystal:1126456975337730078>'
            ).set_thumbnail(
                url=inter.author.display_avatar.url
            )
        )


def setup(client: commands.InteractionBot):
    client.add_cog(Economy(client))