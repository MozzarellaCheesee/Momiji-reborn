from tortoise import fields
from tortoise import models
from tortoise.models import Model

class Warns(Model):
    id = fields.IntField(pk=True)
    profile: fields.ForeignKeyRelation["models.Profiles"] = fields.ForeignKeyField("models.Profiles", related_name="warns", null=False, on_delete=fields.CASCADE)
    reason = fields.CharField(max_length=160, null=True, default=None)

    class Meta:
        table = 'warns'

    def __str__(self):
        return str(self.profile)