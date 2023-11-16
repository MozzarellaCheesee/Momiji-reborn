import dataclasses
from tortoise.models import Model
from main import client

from core.models.authorized_sessions import AuthorizedSessions
from core.models.channels import Channels
from core.models.families import Families
from core.models.profiles import Profiles
from core.models.servers import Servers
from core.models.tickets import Tickets
from core.models.users import Users
from core.models.warns import Warns
from core.models.roles import Roles


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
