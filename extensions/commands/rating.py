import disnake
from disnake import AppCmdInter
from disnake import Localized as __
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from tools.utils import get_member_profile
from tools.exeption import CustomError
from tools.ui.components import StandartView
from tools.ui.leaderboard_select import LeaderBoardSelect

_ = LocalizationStorage('rating')


class Rating(BaseCog):

    @commands.slash_command(name=__("rating", key="COMMAND_GROUP_RATING"),
                            description=__("rating commands", key="COMMAND_GROUP_DESCRIPTION_RATING"))
    async def rating(self, inter: AppCmdInter):
        ...

    @rating.sub_command(
        name=__("leaderboard", key="COMMAND_NAME_LEADERBOARD"),
        description=__("view tops on the server by category", key="COMMAND_DESCRIPTION_LEADERBOARD")
    )
    async def leaderboard(self, inter: AppCmdInter):
        locale = _(inter.locale, "leaderboard")
        server_in_db = await self.client.db.Servers.get(discord_id=inter.guild.id)

        view = StandartView(inter, self.client, timeout=60)
        view.add_item(LeaderBoardSelect(locale, server_in_db, self.client))
        await inter.send(
            embed=disnake.Embed(
                title=locale['title'],
                description=locale['description']
            ).set_thumbnail(
                url=inter.author.display_avatar.url
            ), view=view)

    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
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
                raise CustomError(locale['error'])
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

    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @rating.sub_command(
        name=__("messages", key="COMMAND_NAME_MESSAGES"),
        description=__("set user messages count on server", key="COMMAND_DESCRIPTION_MESSAGES")
    )
    async def messages(
            self,
            inter: AppCmdInter,
            member: disnake.User = commands.Param(
                name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER")
            ),
            messages: int = commands.Param(
                name=__("messages", key="COMMAND_PARAM_NAME_MESSAGES"),
                description=__("select messages", key="COMMAND_PARAM_DESCRIPTION_MESSAGES"),
                ge=0
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
        locale = _(inter.locale, "messages")
        if member.bot:
            raise CustomError(locale['error_bot'])
        profile_in_db = await get_member_profile(member, self.client)
        embed = disnake.Embed(title=locale['title']).set_thumbnail(url=inter.author.display_avatar.url)
        action_in_symbol = {
            "Give": messages,
            "Take": -messages}

        if action == "Set":
            profile_in_db.messages = messages
            embed.description = locale["description_set"]
            embed.add_field(
                name=locale['field_name_1'],
                value=f"> `{messages}`"
            )
        else:
            if (profile_in_db.messages + action_in_symbol[action]) < 0:
                raise CustomError(locale['error'])
            profile_in_db.messages = profile_in_db.messages + action_in_symbol[action]
            embed.description = locale[f"description_{action.lower()}"]
            embed.add_field(
                name=locale['field_name_2'],
                value=f"> `{messages}`",
                inline=False
            ).add_field(
                name=locale['field_name_3'],
                value=f"> `{profile_in_db.messages}`",
                inline=False
            )

        await profile_in_db.save()
        await inter.send(embed=embed)

    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @rating.sub_command(
        name=__("experience", key="COMMAND_NAME_EXPERIENCE"),
        description=__("set user experience count on server", key="COMMAND_DESCRIPTION_EXPERIENCE")
    )
    async def experience(
            self,
            inter: AppCmdInter,
            member: disnake.User = commands.Param(
                name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
                description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER")
            ),
            experience: int = commands.Param(
                name=__("experience", key="COMMAND_PARAM_NAME_EXPERIENCE"),
                description=__("select experience", key="COMMAND_PARAM_DESCRIPTION_EXPERIENCE"),
                ge=0
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
        locale = _(inter.locale, "experience")
        if member.bot:
            raise CustomError(locale['error_bot'])
        profile_in_db = await get_member_profile(member, self.client)
        embed = disnake.Embed(title=locale['title']).set_thumbnail(url=inter.author.display_avatar.url)
        action_in_symbol = {
            "Give": experience,
            "Take": -experience}

        if action == "Set":
            profile_in_db.experience = experience
            embed.description = locale["description_set"]
            embed.add_field(
                name=locale['field_name_1'],
                value=f"> `{experience}`"
            )
        else:
            if (profile_in_db.experience + action_in_symbol[action]) < 0:
                raise CustomError(locale['error'])
            profile_in_db.experience = profile_in_db.experience + action_in_symbol[action]
            embed.description = locale[f"description_{action.lower()}"]
            embed.add_field(
                name=locale['field_name_2'],
                value=f"> `{experience}`",
                inline=False
            ).add_field(
                name=locale['field_name_3'],
                value=f"> `{profile_in_db.experience}`",
                inline=False
            )

        await profile_in_db.save()
        await inter.send(embed=embed)


def setup(client: commands.InteractionBot):
    client.add_cog(Rating(client))
