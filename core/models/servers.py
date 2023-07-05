from tortoise import fields
from tortoise import models
from tortoise.models import Model

class Servers(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.BigIntField(null=False)
    vip = fields.BooleanField(default=False)
    channels: fields.ReverseRelation["models.Channels"]
    tickets: fields.ReverseRelation["models.Tickets"]

    class Meta:
        table = 'servers'

    def __str__(self):
        return str(self.discord_id)