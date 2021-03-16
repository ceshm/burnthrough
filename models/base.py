import json

from peewee import Model, CharField, PostgresqlDatabase, TextField, IntegerField, DateField, ForeignKeyField
from playhouse.postgres_ext import JSONField

with open('config.json') as config_file:
    db_config = json.load(config_file)["database"]

db = PostgresqlDatabase(
    db_config["name"],
    user=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
    port=db_config["port"]
)


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
