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

