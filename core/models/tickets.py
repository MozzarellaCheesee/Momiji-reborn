from tortoise import fields
from tortoise import models
from tortoise.models import Model


class Tickets(Model):
    id = fields.IntField(pk=True)
    profile: fields.ForeignKeyRelation["models.Profiles"] = fields.ForeignKeyField("models.Profiles",
                                                                                   related_name="tickets", null=False,
                                                                                   on_delete=fields.CASCADE)
    server: fields.ForeignKeyRelation["models.Servers"] = fields.ForeignKeyField("models.Servers",
                                                                                 related_name="tickets", null=False,
                                                                                 on_delete=fields.CASCADE)

    class Meta:
        table = 'tickets'

    def __str__(self):
        return str(self.profile)
