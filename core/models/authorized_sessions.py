from tortoise import fields
from tortoise import models
from tortoise.models import Model

class AuthorizedSessions(Model):
    id = fields.IntField(pk=True)
    ip = fields.IntField(null=False)
    user: fields.ForeignKeyRelation["models.Users"] = fields.ForeignKeyField("models.Users", related_name="authorizedsessions", null=False, on_delete=fields.CASCADE)

    class Meta:
        table = 'authorizedsessions'

    def __str__(self):
        return str(self.user)