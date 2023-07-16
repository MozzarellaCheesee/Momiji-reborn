from tortoise import fields
from tortoise import models
from tortoise.models import Model

class Servers(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.BigIntField(null=False)
    vip = fields.BooleanField(default=False)
    renewal_date = fields.DatetimeField(default=None, null=True)
    channels: fields.ReverseRelation["models.Channels"]
    profiles: fields.ReverseRelation["models.Profiles"]
    roles: fields.ReverseRelation["models.Roles"]
    tickets: fields.ReverseRelation["models.Tickets"]
    warns: fields.ReverseRelation["models.Warns"]

    class Meta:
        table = 'servers'

    def __str__(self):
        return str(self.discord_id)
