from extensions.events.__init__ import *

@dataclasses.dataclass
class Models:
    AuthorizedSessions: Model = AuthorizedSessions
    Channels: Model = Channels
    Families: Model = Families
    Profiles: Model = Profiles
    Servers: Model = Servers
    UseTicketsrs: Model = Tickets
    Users: Model = Users
    Warns: Model = Warns

class OnReady(BaseCog):

    @commands.Cog.listener()
    async def on_ready(self):

        self.client.on_error_channel = self.client.get_channel(985268089174233180)
        self.client.report_channel = self.client.get_channel(1125118943959453768)
        self.client.idea_channel = self.client.get_channel(1125118961978183790)

        self.client.db = Models

        self.client.StandartEmbed = standard_emb
        
        self.client.messages_emoji = self.client.get_emoji(1127503836429438976)
        self.client.money_emoji = self.client.get_emoji(1126456975337730078)
        self.client.level_emoji = self.client.get_emoji(1127504341482344489)

        users = self.client.users
        guilds = self.client.guilds

        for user in users:
            if not user.bot:
                await self.client.db.Users.get_or_create(discord_id=user.id)

        for guild in guilds:
            server_in_db = await self.client.db.Servers.get_or_create(discord_id=guild.id)
            for member in guild.members:
                defaults = {
                    "discord_id": user.id
                }
                if not member.bot:
                    user_in_db = await self.client.db.Users.get_or_create(defaults=defaults, discord_id=member.id)
                    if await self.client.db.Profiles.get_or_none(server=server_in_db[0], user=user_in_db[0]) is None:
                        await self.client.db.Profiles.create(user=user_in_db[0], server=server_in_db[0])

        await self.client.change_presence(
            activity=disnake.Streaming(name="Waiting for new members..", url="https://www.twitch.tv/astolfo_oxo"))

        print(f"{self.client.user} is worked stable.")

def setup(client: commands.InteractionBot):
    client.add_cog(OnReady(client))
