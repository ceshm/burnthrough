import json

from peewee import Model, CharField, PostgresqlDatabase, TextField, IntegerField, DateField
from playhouse.postgres_ext import JSONField

db = PostgresqlDatabase('burnthrough', user="cesar", password="cesar2019", host="127.0.0.1", port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class TaskTree(BaseModel):
    name = CharField()
    date = DateField()
    nodes = JSONField()

    def nodes_to_str(self):
        return json.dumps(self.nodes)


class TaskNode(BaseModel):
    text = TextField()
    position = IntegerField()


class User(BaseModel):
    username = CharField()


class UserSession(BaseModel):
    sessionid = CharField(max_length=64)
    device = CharField(max_length=120)



db.connect()
db.create_tables([TaskTree])
