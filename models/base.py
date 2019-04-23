import json

from peewee import Model, CharField, PostgresqlDatabase, TextField, IntegerField, DateField, ForeignKeyField
from playhouse.postgres_ext import JSONField

db = PostgresqlDatabase('burnthrough', user="cesar", password="cesar2019", host="127.0.0.1", port=5432)


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(max_length=255)
    password = CharField(null=True)
    data = JSONField()


class UserSession(BaseModel):
    user = ForeignKeyField(User)
    sessionid = CharField(max_length=64)
    device = CharField(max_length=120)


class UserTaskTree(BaseModel):
    user = ForeignKeyField(User)
    name = CharField()
    date = DateField()
    nodes = JSONField()

    def nodes_to_str(self):
        return json.dumps(self.nodes)


class UserNotes(BaseModel):
    user = ForeignKeyField(User)
    notes = JSONField()

    def notes_to_str(self):
        return json.dumps(self.notes)


db.connect()
db.create_tables([User, UserNotes, UserTaskTree])
