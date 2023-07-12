from tortoise import fields
from tortoise.models import Model
from tortoise import models

class Users(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.BigIntField()
    status = fields.CharField(default=None, null=True, max_length=15)
    authorizedsessions: fields.ReverseRelation["models.AuthorizedSessions"]
    profiles: fields.ReverseRelation["models.Profiles"]


    class Meta:
        table = 'users'

    def __str__(self):
        return str(self.discord_id)