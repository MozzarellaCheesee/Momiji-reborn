from tortoise import fields
from tortoise import models
from tortoise.models import Model


class PrivateVCS(Model):
    id = fields.IntField(pk=True)
    server: fields.ForeignKeyRelation["models.Servers"] = fields.ForeignKeyField("models.Servers",
                                                                                 related_name="private_vcs", null=False,
                                                                                 on_delete=fields.CASCADE)
    owner: fields.ForeignKeyRelation["models.Users"] = fields.ForeignKeyField("models.Users",
                                                                              related_name="owner", null=False,
                                                                              on_delete=fields.CASCADE)
    channel_id = fields.BigIntField(null=False)

    class Meta:
        table = 'private_vcs'

    def __str__(self):
        return str(self.server)
