from extensions.events.__init__ import *

_ = LocalizationStorage('errors')


class OnErrors(BaseCog):

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        # original = error.original
        locale = _(inter.locale, "error")
        stackSummary = traceback.extract_tb(error.__traceback__, limit=20)
        traceback_list = traceback.format_list(stackSummary)

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
            await inter.send(embed=embed, ephemeral=True)
            return

        if isinstance(error, (CustomError, commands.NotOwner)):
            embed.add_field(name=locale["field_name_2"], value=error)
            await inter.send(embed=embed, ephemeral=True)
            return

        embed.description = descriptions_for_err.get(
            50013 if '50013' in str(error) else type(error),
            f"{locale['description']}"
            f"\n```py\n{str(error)}```"
        )

        await inter.send(embed=embed, ephemeral=True, view=SupportButton())
        await self.client.on_error_channel.send(
            embed=disnake.Embed(
                title="Ошибка комманды!",
                description=f"{''.join(traceback_list)} \n\n ```{error.__class__.__name__}: {error}```\n\n Команда вызвана на сервере {inter.guild.name}\nВладелец <@{inter.guild.owner.id}>"
            )
        )

# def setup(client: commands.InteractionBot):
#     client.add_cog(OnErrors(client))
