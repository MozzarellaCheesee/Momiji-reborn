from tortoise import fields
from tortoise import models
from tortoise.models import Model

class Profiles(Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation["models.Users"] = fields.ForeignKeyField("models.Users", related_name="Profile", null=False)
    server: fields.ForeignKeyRelation["models.Servers"] = fields.ForeignKeyField("models.Servers", related_name="Profile", on_delete=fields.CASCADE, null=False)
    family: fields.OneToOneRelation["models.Families"] = fields.OneToOneField("models.Families", related_name="Profile", null=True, on_delete=fields.SET_NULL)
    description = fields.CharField(default=None, null=True, max_length=400)
    level = fields.IntField(default=1, null=False)
    messages = fields.IntField(default=0, null=False)
    experience = fields.IntField(default=0, null=False)
    money = fields.IntField(default=0, null=False)
    warns: fields.ReverseRelation["models.Warns"]
    tickets: fields.ReverseRelation["models.Tickets"]

    class Meta:
        table = 'profiles'

    def __str__(self):
        return str(self.user)