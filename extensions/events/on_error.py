import disnake
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from tools.exeption import CustomError

_ = LocalizationStorage('errors')


class OnErrors(BaseCog):

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):

        locale = _(inter.locale, "error")

        descriptions_for_err = {
            commands.MissingPermissions: locale['descriptions']['0'],
            commands.BotMissingPermissions: locale['descriptions']['1'],
            commands.UserNotFound: locale['descriptions']['2'],
            commands.RoleNotFound: locale['descriptions']['3'],
            50013: locale['descriptions']['4']
        }

        permissions = {
            "administrator": locale["permissions"]['0'],
            "ban_members": locale["permissions"]['1'],
            "kick_members": locale["permissions"]['2'],
            "manage_guild": locale["permissions"]['3'],
            "send_messages": locale["permissions"]['4'],
            "view_channel": locale["permissions"]['5'],
            "manage_roles": locale["permissions"]['6']
        }

        embed = disnake.Embed(
            title=locale['title'],
            color=disnake.Colour.red()
        )

        if isinstance(error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            embed.add_field(
                name=locale['field_name_1'],
                value=", ".join([permissions.get(i, i) for i in error.missing_permissions])
            )

        if isinstance(error, CustomError):
            embed.add_field(name=locale["field_name_2"], value=error)

        embed.description = descriptions_for_err.get(
            50013 if '50013' in str(error) else type(error),
            f"{locale['description']}"
            f"\n```py\n{str(error)}```"
        )

        await inter.send(embed=embed, ephemeral=True)


def setup(client: commands.InteractionBot):
    client.add_cog(OnErrors(client))
