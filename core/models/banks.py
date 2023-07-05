from tortoise import fields
from tortoise import models
from tortoise.models import Model

class Banks(Model):
    id = fields.IntField(pk=True)
    money = fields.IntField(default=0, null=False)
    bank = fields.IntField(default=0, null=False)
    profiles: fields.OneToOneRelation["models.Profiles"]
    
    class Meta:
        table = 'banks'

    def __str__(self):
        return str(self.money, self.bank)