from core.db import BaseMeta
import ormar


class Account(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'accounts'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)
    login: str = ormar.String(max_length=100)
    password: str = ormar.Text()
