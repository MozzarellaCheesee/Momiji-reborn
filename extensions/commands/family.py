import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands
import datetime

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from core.models.families import Families
from core.models.profiles import Profiles
from core.models.servers import Servers
from core.models.users import Users
from tools.utils import get_member_profile_for_marry
from tools.exeption import CustomError
from core.checks import BaseChecks
from tools.utils import love_profile

_ = LocalizationStorage("family")
err = LocalizationStorage('errors#2')


class MarryButtons(disnake.ui.View):

    def __init__(self, author, client: commands.InteractionBot, member, locale: dict, role,
                 check_member: disnake.Member, disnake_author: disnake.Member, inter):
        super().__init__(timeout=60)
        self.author = author
        self.member = member
        self.client = client
        self.locale = locale
        self.role = role
        self.check_member = check_member
        self.disnake_author = disnake_author
        self.inter: AppCmdInter = inter
        self.check = 0

    async def on_timeout(self) -> None:
        if self.check == 1:
            return
        try:
            for children in self.children:
                children.disabled = True
            await self.inter.edit_original_message(view=self)
        except disnake.errors.NotFound:
            return
        except disnake.errors.HTTPException:
            return

    async def interaction_check(self, interaction: disnake.Interaction) -> bool:
        return interaction.author == self.check_member

    @disnake.ui.button(emoji="✅")
    async def yes_callback(self, button, inter: disnake.Interaction):
        role: disnake.Role = inter.guild.get_role(self.role.role_id)
        if role >= self.inter.me.top_role:
            return await inter.edit_original_message(
                embed=disnake.Embed(
                    description=self.locale['errors']['top_role']
                )
            )
        st = datetime.datetime.now()
        date = datetime.datetime.now() + datetime.timedelta(days=30)
        family = await self.client.db.Families.create(
            wife=self.member.user,
            husband=self.author.user,
            date_of_create=date,
            renewal_date=st
        )
        self.author.family = family
        self.member.family = family
        self.author.money -= 5000
        self.author.partner = self.member.user
        self.member.partner = self.author.user
        await self.author.save()
        await self.member.save()
        await inter.response.edit_message(
            embed=disnake.Embed(
                title=self.locale["buttons"]["embeds"]["yes_title"],
                description=self.locale["buttons"]["embeds"]["yes_description"].format(
                    author=self.disnake_author.mention, member=self.check_member.mention)
            ), view=None
        )

        try:
            await self.disnake_author.add_roles(role, reason='marry')
        except disnake.Forbidden:
            ...
        await self.check_member.add_roles(role, reason='marry')

        self.check = 1

    @disnake.ui.button(emoji="❎")
    async def no_callback(self, button, inter: disnake.Interaction):
        await inter.response.edit_message(
            embed=disnake.Embed(
                title=self.locale["buttons"]["embeds"]["no_title"],
                description=self.locale["buttons"]["embeds"]["no_description"].format(author=self.author)
            ), view=None
        )
        self.check = 1


class LoveProfileButtons(disnake.ui.View):

    def __init__(self, inter: AppCmdInter, locale: dict, client: commands.InteractionBot, role):
        super().__init__(timeout=120)
        self.check = 0
        self.inter = inter
        self.locale = locale
        self.client = client
        self.role = role

    async def on_timeout(self) -> None:
        if self.check == 1:
            return
        try:
            for children in self.children:
                children.disabled = True
            await self.inter.edit_original_message(view=self)
        except disnake.errors.NotFound:
            return
        except disnake.errors.HTTPException:
            return

    async def interaction_check(self, interaction: disnake.Interaction) -> bool:
        return interaction.author == self.inter.author

    @disnake.ui.button(emoji="<:momiji_divorce:1175038682818941050>")
    async def divorce_callback(self, button, inter: disnake.Interaction):
        role: disnake.Role = inter.guild.get_role(self.role.role_id)
        if role >= inter.me.top_role:
            return await inter.response.send_message(self.locale["errors"]["top_role"], ephemeral=True)
        server_in_db: tuple[Servers, bool] = await self.client.db.Servers.get_or_create(discord_id=inter.guild.id)
        author_user_in_db: tuple[Users, bool] = await self.client.db.Users.get_or_create(discord_id=inter.author.id)
        author_profile_in_db: Profiles = await self.client.db.Profiles.get(
            user=author_user_in_db[0], server=server_in_db[0]
        )
        author_profile_in_db: Profiles = await author_profile_in_db.filter(
            server=server_in_db[0], user=author_user_in_db[0]).first().prefetch_related('family')
        family: Families = await author_profile_in_db.family.first().prefetch_related('wife', 'husband')
        if family.husband == author_user_in_db[0]:
            member: disnake.Member = inter.guild.get_member(family.wife.discord_id)
            member_in_db: Profiles = await self.client.db.Profiles.get(server=server_in_db[0],
                                                                       user=await family.wife)
        else:
            member: disnake.Member = inter.guild.get_member(family.husband.discord_id)
            member_in_db: Profiles = await self.client.db.Profiles.get(server=server_in_db[0],
                                                                       user=await family.husband)
        author_profile_in_db.partner = None
        member_in_db.partner = None
        await author_profile_in_db.save()
        await member_in_db.save()
        await self.client.db.Families.filter(id=family.id).delete()
        await inter.author.remove_roles(role)
        await member.remove_roles(role)

        await inter.response.edit_message(
            attachments=[],
            embed=disnake.Embed(
                title=self.locale["divorce_title"].format(author=inter.author.display_name, member=member.display_name),
                description=self.locale["divorce_description"]
            ).set_image(
                url="https://media.tenor.com/sGFqg02n95oAAAAC/kana-arima-oshi-no-ko.gif"
            ), view=None
        )

    @disnake.ui.button(emoji="🏦")
    async def bank_callback(self, button, inter: disnake.Interaction):
        ...


class Family(BaseCog):

    @commands.slash_command(name=__("family", key="COMMAND_GROUP_FAMILY"),
                            description=__("family's commands", key="COMMAND_GROUP_DESCRIPTION_FAMILY"))
    async def family(self, inter: AppCmdInter):
        ...

    @BaseChecks.self_check(err)
    @BaseChecks.bot_check(err)
    @family.sub_command(
        name=__('marry', key="COMMAND_NAME_MARRY"),
        description=__('marry command (cost 5000)', key="COMMAND_DESCRIPTION_MARRY")
    )
    async def marry(self, inter: AppCmdInter,
                    user: disnake.User = commands.Param(
                        name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                        description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"))
                    ):
        locale = _(inter.locale, "marry")
        author_profile = await get_member_profile_for_marry(inter.author, self.client)

        if author_profile is None:
            return await inter.send(locale['error_'], ephemeral=True)

        member_profile = await get_member_profile_for_marry(user, self.client)

        if member_profile is None:
            return await inter.send(locale['error__'], ephemeral=True)

        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.guild.id)
        role = await self.client.db.Roles.get_or_none(server=server_in_db[0], role_type="MARRY")
        if role is None:
            raise CustomError(locale["errors"]["not_role"])
        if author_profile.family is not None:
            raise CustomError(locale["errors"]["author_married"])
        if member_profile.family is not None:
            raise CustomError(locale["errors"]["member_married"])
        if author_profile.money < 5000:
            raise CustomError(locale["errors"]["not_money"])
        await inter.send(
            user.mention,
            embed=disnake.Embed(
                title=locale["title"],
                description=locale["description"].format(user=user.mention, author=inter.author.mention)
            ), view=MarryButtons(author_profile, self.client, member_profile, locale, role, user, inter.author, inter)
        )

    @family.sub_command(
        name=__('love-profile', key="COMMAND_NAME_LOVE"),
        description=__('view love profile', key="COMMAND_DESCRIPTION_LOVE")
    )
    async def loveprofile(
            self, inter: AppCmdInter,
            member: disnake.Member = commands.Param(
                name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
                default=lambda inter: inter.author
            )
    ):
        locale = _(inter.locale, "love_profile")
        loc = err(inter.locale, "errors")
        if member.bot:
            raise CustomError(loc['bot_error'])
        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.guild.id)
        role = await self.client.db.Roles.get_or_none(server=server_in_db[0], role_type="MARRY")
        if role is None:
            raise CustomError(locale["errors"]["not_role"])
        await love_profile(locale, self.client, inter, member, LoveProfileButtons(inter, locale, self.client, role))


def setup(client: commands.InteractionBot):
    client.add_cog(Family(client))
