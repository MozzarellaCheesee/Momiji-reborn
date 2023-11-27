import disnake
from disnake import AppCmdInter
from disnake.ext import commands
from disnake.i18n import Localised as __

from core.cog import BaseCog
from core.models.channels import Channels
from core.models.roles import Roles
from core.models.servers import Servers

from tools.exeption import CustomError
from core.i18n import LocalizationStorage
from tools.ui.modals.server_settings_verefy import VerefySetupModal

_ = LocalizationStorage("server_settings")

EMOJI: dict = {
    True: "<a:Toggleon:1175843384766779393>",
    False: "<a:Toggleoff:1175843484020785152>"
}


class ServerSettings(BaseCog):

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name=__("server", key="COMMAND_GROUP_SERVER"),
                            description=__("server setup commands", key="COMMAND_GROUP_DESCRIPTION_SERVER"))
    async def server(self, inter: AppCmdInter):
        ...

    @commands.bot_has_permissions(moderate_members=True, manage_roles=True)
    @server.sub_command(name=__("verify", key="COMMAND_NAME_VEREFY"),
                        description=__("set verification on your server", key="COMMAND_DESCRIPTION_VEREFY"))
    async def set_verefy(
            self, inter: AppCmdInter,
            channel: disnake.TextChannel = commands.Param(
                name=__("channel", key="COMMAND_PARAM_NAME_CHANNEL"),
                description=__("select channel", key="COMMAND_PARAM_DESCRIPTION_CHANNEL")
            )
    ):
        locale = _(inter.locale, "verefy")
        server_in_db = await self.client.db.Servers.get_or_create(discord_id=inter.guild.id)
        role = await self.client.db.Roles.get_or_none(server=server_in_db[0], role_type="VERIFY")
        if role is None:
            raise CustomError(locale["not_role"])
        await inter.response.send_modal(VerefySetupModal(locale, _, self.client, channel))

    @server.sub_command(name=__("verify-role", key="COMMAND_NAME_VEREFY-ROLE"),
                        description=__("set verify-role", key="COMMAND_DESCRIPTION_VEREFY-ROLE"))
    async def set_verify_role(
            self, inter: AppCmdInter,
            role: disnake.Role = commands.Param(
                name=__("role", key="COMMAND_PARAM_NAME_ROLE"),
                description=__("select role", key="COMMAND_PARAM_DESCRIPTION_ROLE")
            ),
            action: str = commands.Param(
                name=__("action", key="COMMAND_PARAM_NAME_ACTION"),
                description=__("select an action", key="COMMAND_PARAM_DESCRIPTION_ACTION"),
                choices=[
                    __("set", key="SET"),
                    __("delete", key="DELETE")
                ],
                default="set")
    ):
        locale = _(inter.locale, "set_verefy_role")

        if role >= inter.me.top_role:
            raise CustomError(locale['error'])

        server_in_db: tuple[Servers, bool] = await self.client.db.Servers.get_or_create(discord_id=inter.guild.id)
        role_in_db: Roles | None = await self.client.db.Roles.get_or_none(server=server_in_db[0],
                                                                          role_type="VERIFY")

        if action == "delete":
            if role_in_db is not None:
                server_in_db[0].verify_role = False
                await server_in_db[0].save()
                await role_in_db.delete()
                return await inter.send(
                    embed=disnake.Embed(
                        title=locale['delete']['title'],
                        description=locale['delete']['description']
                    ),
                    ephemeral=True
                )
            else:
                return await inter.send(
                    embed=disnake.Embed(
                        title=locale['delete']['error']
                    ),
                    ephemeral=True
                )

        if role_in_db is None:
            await self.client.db.Roles.create(server=server_in_db[0], role_type="VERIFY", role_id=role.id)
        else:
            role_in_db.role_id = role.id
            await role_in_db.save()

        server_in_db[0].verify_role = True
        await server_in_db[0].save()

        await inter.send(
            embed=disnake.Embed(
                title=locale["title"],
                description=locale["description"].format(role=role.mention)
            ), ephemeral=True
        )

    @server.sub_command(name=__("marry-role", key="COMMAND_NAME_MARRY-ROLE"),
                        description=__("set marry-role", key="COMMAND_DESCRIPTION_MARRY-ROLE"))
    async def set_marry_role(
            self, inter: AppCmdInter,
            role: disnake.Role = commands.Param(
                name=__("role", key="COMMAND_PARAM_NAME_ROLE"),
                description=__("select role", key="COMMAND_PARAM_DESCRIPTION_ROLE")
            ),
            action: str = commands.Param(
                name=__("action", key="COMMAND_PARAM_NAME_ACTION"),
                description=__("select an action", key="COMMAND_PARAM_DESCRIPTION_ACTION"),
                choices=[
                    __("set", key="SET"),
                    __("delete", key="DELETE")
                ],
                default="set")
    ):
        locale = _(inter.locale, "set_marry_role")

        if role >= inter.me.top_role:
            raise CustomError(locale['error'])

        server_in_db: tuple[Servers, bool] = await self.client.db.Servers.get_or_create(discord_id=inter.guild.id)
        role_in_db: Roles | None = await self.client.db.Roles.get_or_none(server=server_in_db[0],
                                                                          role_type="MARRY")

        if action == "delete":
            if role_in_db is not None:
                server_in_db[0].verify_role = False
                await server_in_db[0].save()
                await role_in_db.delete()
                return await inter.send(
                    embed=disnake.Embed(
                        title=locale['delete']['title'],
                        description=locale['delete']['description']
                    ),
                    ephemeral=True
                )
            else:
                return await inter.send(
                    embed=disnake.Embed(
                        title=locale['delete']['error']
                    ),
                    ephemeral=True
                )

        if role_in_db is None:
            await self.client.db.Roles.create(server=server_in_db[0], role_type="MARRY", role_id=role.id)
        else:
            role_in_db.role_id = role.id
            await role_in_db.save()

        server_in_db[0].married_role = True
        await server_in_db[0].save()

        await inter.send(
            embed=disnake.Embed(
                title=locale["title"],
                description=locale["description"].format(role=role.mention)
            ), ephemeral=True
        )

    @server.sub_command(name=__("private-rooms", key="COMMAND_NAME_PRIVATE_ROOMS"),
                        description=__("set private_rooms", key="COMMAND_DESCRIPTION_PRIVATE_ROOMS"))
    async def create_rooms_object(self, inter: AppCmdInter,
                                  action: str = commands.Param(
                                      name=__("action", key="COMMAND_PARAM_NAME_ACTION"),
                                      description=__("select an action", key="COMMAND_PARAM_DESCRIPTION_ACTION"),
                                      choices=[
                                          __("set", key="SET"),
                                          __("delete", key="DELETE")
                                      ],
                                      default=None)
                                  ):
        locale = _(inter.locale, "create_rooms_object")
        server_in_db: tuple[Servers, bool] = await self.client.db.Servers.get_or_create(discord_id=inter.guild.id)
        channel_in_db: Channels | None = await self.client.db.Channels.get_or_none(server=server_in_db[0],
                                                                                   channel_type="VoicesChannel")
        if action == "delete" or action == "удалить":
            if channel_in_db is not None:
                server_in_db[0].private_vcs_channel = False
                old_channel: disnake.VoiceChannel = inter.guild.get_channel(channel_in_db.channel_id)
                await channel_in_db.delete()
                try:
                    await old_channel.delete()
                except AttributeError:
                    ...
                return await inter.send(
                    embed=disnake.Embed(
                        title=locale['delete']['title'],
                        description=locale['delete']['description']
                    ),
                    ephemeral=True
                )
            else:
                return await inter.send(
                    embed=disnake.Embed(
                        title=locale['delete']['error']
                    ),
                    ephemeral=True
                )

        if channel_in_db is not None:
            server_in_db[0].private_vcs_channel = True
            old_channel: disnake.VoiceChannel = inter.guild.get_channel(channel_in_db.channel_id)
            await channel_in_db.delete()
            try:
                await old_channel.delete()
            except AttributeError:
                ...

        new_channel: disnake.VoiceChannel = await inter.guild.create_voice_channel(name="Create [ + ]", user_limit=2)

        await self.client.db.Channels.create(server=server_in_db[0],
                                             channel_id=new_channel.id, channel_type="VoicesChannel")
        await server_in_db[0].save()

        await inter.send(
            embed=disnake.Embed(
                title=locale['set']['title'],
                description=locale['set']['description'].format(channel=new_channel.mention)
            ),
            ephemeral=True
        )

    @server.sub_command(name=__("server-settings-info", key="COMMAND_NAME_SERVER_SETTINGS"),
                        description=__("information about server's settings",
                                       key="COMMAND_DESCRIPTION_SERVER_SETTINGS"))
    async def server_settings(self, inter: AppCmdInter):
        locale = _(inter.locale, "server_settings_info")
        server_in_db: tuple[Servers, bool] = await self.client.db.Servers.get_or_create(discord_id=inter.guild.id)
        settings = [server_in_db[0].vip, server_in_db[0].logs, server_in_db[0].verify,
                    server_in_db[0].private_vcs_channel, server_in_db[0].married_role, server_in_db[0].verify_role]
        embed = disnake.Embed(
            title=locale['title'],
            description=locale['description']
        )

        for i, setting in enumerate(settings, start=1):
            embed.add_field(
                name=locale[f'field_name_{i}'],
                value=f"{locale[f'field_description_{i}']}\n{locale['state']}: {EMOJI[setting]}"
            )

        await inter.send(embed=embed)


def setup(client: commands.InteractionBot):
    client.add_cog(ServerSettings(client))
