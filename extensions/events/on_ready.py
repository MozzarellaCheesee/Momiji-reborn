from extensions.events.__init__ import *

@dataclasses.dataclass
class Models:
    AuthorizedSessions: Model = AuthorizedSessions
    Banks: Model = Banks
    Channels: Model = Channels
    Families: Model = Families
    Profiles: Model = Profiles
    Servers: Model = Servers
    UseTicketsrs: Model = Tickets
    Users: Model = Users
    Warns: Model = Warns

class BotActivity(BaseCog):

    @commands.Cog.listener()
    async def on_ready(self):

        self.client.on_error_channel = self.client.get_channel(985268089174233180)
        self.client.report_channel = self.client.get_channel(1125118943959453768)
        self.client.idea_channel = self.client.get_channel(1125118961978183790)
        self.client.db = Models


        users = self.client.users
        guilds = self.client.guilds

        for user in users:
            if not user.bot:
                await self.client.db.Users.get_or_create(discord_id=user.id)

        for guild in guilds:
            await self.client.db.Servers.get_or_create(discord_id=guild.id)
            for user in guild.members:
                if not user.bot:
                    user_in_db = await self.client.db.Users.get(discord_id=user.id)
                    server_in_db = await self.client.db.Servers.get(discord_id=guild.id)
                    if await self.client.db.Profiles.get_or_none(user=user_in_db, server=server_in_db) is None:
                        bank = await self.client.db.Banks.create()
                        await self.client.db.Profiles.create(user=user_in_db, server=server_in_db, bank=bank, family=None)

        await self.client.change_presence(
            activity=disnake.Streaming(name="Waiting for new members..", url="https://www.twitch.tv/astolfo_oxo"))

        print(f"{self.client.user} is worked stable.")

def setup(client: commands.InteractionBot):
    client.add_cog(BotActivity(client))
