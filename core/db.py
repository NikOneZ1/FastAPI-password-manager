import databases
import ormar
import sqlalchemy as sa
from core.settings import *

POSTGRESQL_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"

database = databases.Database(POSTGRESQL_URI)
metadata = sa.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata
