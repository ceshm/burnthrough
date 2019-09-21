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
    expanded_nodes = JSONField(default=[])

    def nodes_to_str(self):
        return json.dumps(self.nodes)

    def expanded_nodes_to_str(self):
        return json.dumps(self.expanded_nodes)


class UserNotes(BaseModel):
    user = ForeignKeyField(User)
    notes = JSONField()

    def notes_to_str(self):
        return json.dumps(self.notes)


class UserDailyData(BaseModel):
    user = ForeignKeyField(User)
    date = DateField()
    data = JSONField()
    """
    data = {
        "levels": {
            "sleep": 8.5,
            "caffeine": 2,
            "zen(calmness)": 5,
        },
        "annotations": { ... }
    }
    """

    def data_to_str(self):
        return json.dumps(self.data)

    @property
    def levels(self):
        if self.data and "levels" in self.data:
            return self.data["levels"]
        else:
            return None


# Obsolete
class UserExpandedNodes(BaseModel):
    user = ForeignKeyField(User)
    data = JSONField()

    def data_to_str(self):
        return json.dumps(self.data)


db.connect()
#db.create_tables([User, UserNotes, UserTaskTree])
#db.create_tables([UserExpandedNodes])
#db.create_tables([UserDailyData])
db.create_tables([UserSession])
