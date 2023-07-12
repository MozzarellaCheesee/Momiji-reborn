import disnake
from disnake import AppCmdInter
from disnake.ext import commands
from core.cog import BaseCog
from tools.exeption import CustomError
from core.i18n import LocalizationStorage
from disnake.i18n import Localised as __

from tools.ui.modals.server_settings_verefy import VerefySetupModal

_ = LocalizationStorage("server_settings")

async def get_or_create_role(client: commands.InteractionBot, server: any, _type: str, defaults: dict):
    _server = await client.db.Servers.get(discord_id=server.id)
    defaults["server"] = _server
    role = await client.db.Roles.get_or_create(defaults=defaults, role_type=_type, server_id=_server.id)
    return role

class ServerSettings(BaseCog):

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name=__("server", key="COMMAND_GROUP_SERVER"),
                            description=__("server setup commands", key="COMMAND_GROUP_DESCRIPTION_SERVER"))
    async def server(self, inter: AppCmdInter):
        ...

    @commands.bot_has_permissions(moderate_members=True, manage_roles=True)
    @server.sub_command(name=__("verefy", key="COMMAND_NAME_VEREFY"),
                         description=__("set verification on your server", key="COMMAND_DESCRIPTION_VEREFY"))
    async def set_verefy(
        self, inter: AppCmdInter, 
        channel:disnake.TextChannel = commands.Param(
            name=__("channel", key="COMMAND_PARAM_NAME_CHANNEL"),
            description=__("select channel", key="COMMAND_PARAM_DESCRIPTION_CHANNEL")
        )
    ):
        locale = _(inter.locale, "verefy")
        server_in_db = await self.client.db.Servers.get(discord_id=inter.guild.id)
        role = await self.client.db.Roles.get_or_none(server=server_in_db, role_type="VEREFY")
        if role is None:
            raise CustomError(locale["not_role"])
        await inter.response.send_modal(VerefySetupModal(locale, _, self.client, channel))

    @server.sub_command(name=__("verefy-role", key="COMMAND_NAME_VEREFY-ROLE"),
                         description=__("set verefy-role", key="COMMAND_DESCRIPTION_VEREFY-ROLE"))
    async def set_verefy_role(
        self, inter: AppCmdInter, 
        role: disnake.Role = commands.Param(
            name=__("role", key="COMMAND_PARAM_NAME_ROLE"),
            description=__("select role", key="COMMAND_PARAM_DESCRIPTION_ROLE")
        )
    ):
        locale = _(inter.locale, "set_verefy_role")
        defaults = {
            "role_id": role.id
        }
        _role = await get_or_create_role(self.client, inter.guild, "VEREFY", defaults)
        if _role[1] is False:
            _role[0].role_id = role.id
            await _role[0].save()
            
        await inter.send(
            embed = disnake.Embed(
                title=locale["title"],
                description=locale["description"].format(role=role.mention)
            )
        )


def setup(client: commands.InteractionBot):
    client.add_cog(ServerSettings(client))