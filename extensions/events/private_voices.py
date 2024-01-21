import disnake
from disnake.errors import Forbidden
from disnake.ext import commands

from core.cog import BaseCog
from core.models.channels import Channels
from core.models.private_vc import PrivateVCS
from core.models.servers import Servers
from core.models.users import Users


class PrivateVoices(BaseCog):

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState,
                                    after: disnake.VoiceState):
        if member.bot:
            return

        try:
            server_in_db: tuple[Servers, bool] = await self.client.db.Servers.get_or_create(discord_id=member.guild.id)
            _server_in_db: list[Servers] = await server_in_db[0].all().filter(
                discord_id=server_in_db[0].discord_id).prefetch_related("channels")

            if before.channel is not None and len(before.channel.members) < 1:
                private_vc: PrivateVCS = await self.client.db.PrivateVCS.get_or_none(server=server_in_db[0],
                                                                                     channel_id=before.channel.id)
                if private_vc is not None:
                    await private_vc.delete()
                    await before.channel.delete()

            channel: list[Channels] = await _server_in_db[0].channels

            if len(channel) < 1:
                return

            channel_: Channels = await channel[0].filter(server=server_in_db[0], channel_type="VoicesChannel").first()

            if not channel:
                return

            channel_obj: disnake.VoiceChannel = member.guild.get_channel(int(channel_.channel_id))

            if after.channel == channel_obj:
                user_in_db: tuple[Users, bool] = await self.client.db.Users.get_or_create(discord_id=member.id)
                permissions = {member: disnake.PermissionOverwrite(manage_webhooks=True, priority_speaker=True)}
                new_channel = await member.guild.create_voice_channel(name=f"{member.display_name}", user_limit=5,
                                                                      category=channel_obj.category,
                                                                      overwrites=permissions)
                await self.client.db.PrivateVCS.create(server=server_in_db[0],
                                                       owner=user_in_db[0], channel_id=new_channel.id)
                await member.move_to(new_channel)
        except AttributeError:
            ...
        except Forbidden:
            try:
                await member.send("**The bot has no rights to create channels on the server**\n"
                                  "**У бота нет прав для создания каналов на сервере**")
            except:
                await member.guild.owner.send("**The bot has no rights to create channels on the server**\n"
                                              "**У бота нет прав для создания каналов на сервере**")


def setup(client: commands.InteractionBot):
    client.add_cog(PrivateVoices(client))
