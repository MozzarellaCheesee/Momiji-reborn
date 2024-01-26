import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from random import randint, getrandbits

from core.cog import BaseCog
from core.checks import BaseChecks
from core.i18n import LocalizationStorage
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

        user_in_db = await self.client.db.Users.get_or_create(discord_id=inter.author.id)
        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.author.guild.id)
        profile = await self.client.db.Profiles.get_or_none(user=user_in_db[0], server=server_in_db[0])

        if not profile:
            return await inter.send(locale['error'], ephemeral=True)

        profile.money = profile.money + money

        embed = disnake.Embed(title=locale["title"], description=locale["description"])\
            .add_field(name=locale["field_name_1"], value=f'> `{money}` <a:momiji_crystal:1126456975337730078>')\
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
    async def roulette(self, inter: AppCmdInter,
                       bullets: int = commands.Param(name=__("bullets", key="bullets"),
                                                     description=__("enter bullets count", key="bullets_desc"), le=5,
                                                     ge=1),
                       amount: int = commands.Param(name=__("stake", key="money"),
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
                             .add_field(name=locale["summ_lose"], value=amount)
                             .add_field(name=locale["balance"], value=author_profile.money)
                             .set_thumbnail(url=inter.author.display_avatar))
        else:
            author_profile.money += amount * (bullets+1) - amount
            await author_profile.save()
            await inter.send(embed=disnake.Embed(title=locale["win_title"], description=locale["win_description"])
                             .add_field(name=locale["summ_win"], value=amount * (bullets+1) - amount)
                             .add_field(name=locale["balance"], value=author_profile.money)
                             .set_thumbnail(url=inter.author.display_avatar))


def setup(client: commands.InteractionBot):
    client.add_cog(Economy(client))
