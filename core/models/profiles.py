from __future__ import annotations

from tortoise import fields
from tortoise.queryset import Prefetch
from tortoise.exceptions import DoesNotExist
from tortoise import models
from tortoise.models import Model

from .users import Users
from .servers import Servers
from .banks import Banks

class Profiles(Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation["models.Users"] = fields.ForeignKeyField("models.Users", related_name="Profile", null=False)
    server: fields.ForeignKeyRelation["models.Servers"] = fields.ForeignKeyField("models.Servers", related_name="Profile", on_delete=fields.CASCADE, null=False)
    bank: fields.OneToOneRelation["models.Banks"] = fields.OneToOneField("models.Banks", related_name="Profile", null=False, on_delete=fields.CASCADE)
    family: fields.OneToOneRelation["models.Families"] = fields.OneToOneField("models.Families", related_name="Profile", null=True, on_delete=fields.SET_NULL)
    level = fields.IntField(default=1, null=False)
    messages = fields.IntField(default=0, null=False)
    experience = fields.IntField(default=0, null=False)
    warns: fields.ReverseRelation["models.Warns"]
    tickets: fields.ReverseRelation["models.Tickets"]

    class Meta:
        table = 'profiles'

    def __str__(self):
        return str(self.user)

    @classmethod
    async def get_profile_or_create(cls, member_id: int,
                                    server_id: int,
                                    to_prefetch: list[str | Prefetch] = None,
                                    **kwargs) -> tuple[Profiles, bool]:
        user = await Users.get_or_create(discord_id=member_id)
        server = await Servers.get_or_create(discord_id=server_id)
        try:
            return await (cls.get(user=user, server=server, **kwargs).prefetch_related(*to_prefetch) if to_prefetch else cls.get(user=user, server=server, **kwargs)), True
        except DoesNotExist:
            bank = await Banks.create()
            return await cls.create(user=user, sever=server, bank=bank), False