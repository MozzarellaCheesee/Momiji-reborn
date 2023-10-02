from tortoise import fields
from tortoise import models
from tortoise.models import Model

class Roles(Model):
    id = fields.IntField(pk=True)
    server: fields.ForeignKeyRelation["models.Servers"] = fields.ForeignKeyField("models.Servers", related_name="roles", null=False, on_delete=fields.CASCADE)
    role_id = fields.BigIntField(null=False)
    role_type = fields.CharField(max_length=15, null=False)

    class Meta:
        table = 'roles'

    def __str__(self):
        return str(self.server)