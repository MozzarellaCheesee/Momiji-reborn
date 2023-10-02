from extensions.events.__init__ import *

_ = LocalizationStorage("server_settings")

@dataclasses.dataclass
class Models:
    AuthorizedSessions: Model = AuthorizedSessions
    Channels: Model = Channels
    Families: Model = Families
    Profiles: Model = Profiles
    Servers: Model = Servers
    Tickets: Model = Tickets
    Users: Model = Users
    Warns: Model = Warns
    Roles: Model = Roles

@dataclasses.dataclass
class Channels:
    on_error_channel = client.get_channel(985268089174233180)
    report_channel = client.get_channel(1125118943959453768)
    idea_channel = client.get_channel(1125118961978183790)
    log_join_channel = client.get_channel(978325826753953975)
    log_remove_channel = client.get_channel(978620072014782515)

@dataclasses.dataclass
class Emojies:
    messages_emoji = client.get_emoji(1127503836429438976)
    money_emoji = client.get_emoji(1126456975337730078)
    level_emoji = client.get_emoji(1127504341482344489)

class OnReady(BaseCog):

    @commands.Cog.listener()
    async def on_ready(self):

        self.client.channels = Channels
        self.client.db = Models
        self.client.emojies = Emojies

        for user in self.client.users:
            if not user.bot:
                await self.client.db.Users.get_or_create(discord_id=user.id)

        for guild in self.client.guilds:
            server_in_db = await self.client.db.Servers.get_or_create(discord_id=guild.id)
            for member in guild.members:
                if not member.bot:
                    user_in_db = await self.client.db.Users.get(discord_id=member.id)
                    if await self.client.db.Profiles.get_or_none(server=server_in_db[0], user=user_in_db) is None:
                        await self.client.db.Profiles.create(user=user_in_db, server=server_in_db[0])

        await self.client.change_presence(
            activity=disnake.Streaming(name="Waiting for new members..", url="https://www.twitch.tv/astolfo_oxo"))

        self.client.add_view(view=VerefyButton(self.client, _))

        print(
            f"\033[38;5;38m[CLIENT] \033[38;5;67m⌗ \033[38;5;105m{self.client.user}\033[0;0m is worked stable.\n"
            f"----------------------------------------------"
        )
        logging.info("Бот был запущен")

def setup(client: commands.InteractionBot):
    client.add_cog(OnReady(client))
