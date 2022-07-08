import os
import databases
import ormar
import sqlalchemy as sa

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")

POSTGRESQL_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"

database = databases.Database(POSTGRESQL_URI)
metadata = sa.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata
