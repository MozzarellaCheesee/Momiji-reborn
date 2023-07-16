import disnake
from disnake import AppCmdInter, UserCommandInteraction
from disnake import Localized as __
from disnake.ext import commands
import datetime

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from tools.utils import get_member_profile_for_marry, get_or_create_role
from tools.exeption import CustomError
from core.checks import BaseChecks


_ = LocalizationStorage("family")
err = LocalizationStorage('errors#2')

class MarryButtons(disnake.ui.View):
    
    def __init__(self, author, client: commands.InteractionBot, member, locale: dict, role: disnake.Role, check_member: disnake.Member, disnake_author: disnake.Member, inter):
        super().__init__(timeout=60)
        self.author = author
        self.member = member
        self.client = client
        self.locale = locale
        self.role = role
        self.check_member = check_member
        self.disnake_author = disnake_author
        self.inter = inter
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
        self.author.money -= 12000
        self.author.partner = self.member.user
        self.member.partner = self.author.user
        await self.author.save() 
        await self.member.save()
        await inter.response.edit_message(
            embed=disnake.Embed(
                title=self.locale["buttons"]["embeds"]["yes_title"],
                description=self.locale["buttons"]["embeds"]["yes_description"].format(author=self.disnake_author.mention, member=self.check_member.mention)
            ), view=None
        )

        await self.disnake_author.add_roles(role, reason='marry')
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

class Family(BaseCog):
    
    @commands.slash_command(name=__("family", key="COMMAND_GROUP_FAMILY"),
                            description=__("family's commands", key="COMMAND_GROUP_DESCRIPTION_FAMILY"))
    async def family(self, inter: AppCmdInter):
        ...

    @BaseChecks.self_check(err)
    @BaseChecks.bot_check(err)
    @family.sub_command(
        name=__('marry', key="COMMAND_NAME_MARRY"),
        description=__('marry command', key="COMMAND_DESCRIPTION_MARRY")
    )
    async def marry(self, inter: AppCmdInter,
                   user: disnake.User = commands.Param(
                        name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                        description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"))
    ):
        locale = _(inter.locale, "marry")
        author_profile = await get_member_profile_for_marry(inter.author, self.client)
        member_profile = await get_member_profile_for_marry(user, self.client)
        server_in_db = await self.client.db.Servers.get(discord_id=inter.guild.id)
        role = await self.client.db.Roles.get_or_none(server=server_in_db, role_type="MARRY")
        if role is None:
            raise CustomError(locale["errors"]["not_role"])
        if author_profile.family is not None:
            raise CustomError(locale["errors"]["author_married"])
        if member_profile.family is not None:
            raise CustomError(locale["errors"]["member_married"])
        if author_profile.money < 12000:
            raise CustomError(locale["errors"]["not_money"])
        await inter.send(
            user.mention,
            embed = disnake.Embed(
                title=locale["title"],
                description=locale["description"].format(user=user.mention, author=inter.author.mention)
            ), view=MarryButtons(author_profile, self.client, member_profile, locale, role, user, inter.author, inter)
        )
    
def setup(client: commands.InteractionBot):
    client.add_cog(Family(client))