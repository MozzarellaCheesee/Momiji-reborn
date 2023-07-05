from tortoise import fields
from tortoise import models
from tortoise.models import Model

class Channels(Model):
    id = fields.IntField(pk=True)
    server: fields.ForeignKeyRelation["models.Servers"] = fields.ForeignKeyField("models.Servers", related_name="channles", null=False, on_delete=fields.CASCADE)
    channel_id = fields.BigIntField(null=False)
    channel_type = fields.CharField(max_length=15, null=False)

    class Meta:
        table = 'channels'

    def __str__(self):
        return str(self.server)