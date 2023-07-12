from tortoise import fields
from tortoise import models
from tortoise.models import Model

class Families(Model):
    id = fields.IntField(pk=True)
    wife: fields.ForeignKeyRelation["models.Users"] = fields.ForeignKeyField("models.Users", related_name="Families_w", null=False)
    husband: fields.ForeignKeyRelation["models.Users"] = fields.ForeignKeyField("models.Users", related_name="Families_h", null=False)
    money = fields.IntField(default=0, null=False)
    channel_id = fields.BigIntField(null=False)
    date_of_create = fields.DatetimeField()
    renewal_date = fields.DatetimeField()

    class Meta:
        table = 'families'

    def __str__(self):
        return str(self.wife, self.husband)