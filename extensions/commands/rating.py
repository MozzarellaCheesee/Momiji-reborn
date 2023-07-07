import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from tools.utils import get_member_profile
from tools.exeption import CustomError

_ =LocalizationStorage('rating')

class Rating(BaseCog):

    @commands.slash_command(name=__("rating", key="COMMAND_GROUP_RATING"),
                            description=__("rating commands", key="COMMAND_GROUP_DESCRIPTION_RATING"))
    async def rating(self, inter: AppCmdInter):
        ...
    
    @rating.sub_command(
        name=__("level", key="COMMAND_NAME_LEVEL"),
        description=__("set user level on server", key="COMMAND_DESCRIPTION_LEVEL")
    )
    async def level(
        self, 
        inter: AppCmdInter,
        member: disnake.User = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER")
        ),
        level: int = commands.Param(
            name=__("level", key="COMMAND_PARAM_NAME_LEVEL"),
            description=__("select level", key="COMMAND_PARAM_DESCRIPTION_LEVEL"),
            ge=1
        ),
        action: str = commands.Param(
            name=__("action", key="COMMAND_PARAM_NAME_ACTION"),
            description=__("select action", key="COMMAND_PARAM_DESCRIPTION_ACTION"),
            choices=[
                __("Give", key="COMMAND_PARAM_CHOISE_GIVE"),
                __("Take", key="COMMAND_PARAM_CHOISE_TAKE"),
                __("Set", key="COMMAND_PARAM_CHOISE_SET")
            ]
        )
    ):
        locale = _(inter.locale, "level")
        if member.bot:
            raise CustomError(locale['error'])
        profile_in_db = await get_member_profile(member, self.client)
        embed = disnake.Embed(title=locale['title']).set_thumbnail(url=inter.author.display_avatar.url)
        action_in_symbol = {
            "Give": level,
            "Take": -level}

        if action == "Set":
            profile_in_db.level = level
            profile_in_db.experience = 0
            embed.description = locale["description_set"]
            embed.add_field(
                name=locale['field_name_1'],
                value=f"> `{level}`"
            )
        else:
            if (profile_in_db.level + action_in_symbol[action]) < 1:
                raise CustomError("Уровень не может быть меньше одного")
            profile_in_db.level = profile_in_db.level + action_in_symbol[action]
            profile_in_db.experience = 0
            embed.description = locale[f"description_{action.lower()}"]
            embed.add_field(
                name=locale['field_name_2'],
                value=f"> `{level}`",
                inline=False
            ).add_field(
                name=locale['field_name_3'],
                value=f"> `{profile_in_db.level}`",
                inline=False
            )
        
        await profile_in_db.save()
        await inter.send(embed=embed)
            

        


        

def setup(client: commands.InteractionBot):
    client.add_cog(Rating(client))