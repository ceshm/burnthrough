from peewee import PostgresqlDatabase
from playhouse.migrate import PostgresqlMigrator, migrate
from playhouse.postgres_ext import JSONField

db = PostgresqlDatabase('burnthrough', user="cesar", password="cesar2019", host="127.0.0.1", port=5432)
migrator = PostgresqlMigrator(db)


migrate(
    migrator.add_column('usertasktree', 'expanded_nodes', JSONField(default=[])),
)
