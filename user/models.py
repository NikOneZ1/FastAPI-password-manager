import ormar

from core.db import BaseMeta
from core.settings import SECRET_KEY


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'users'

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100, unique=True)
    email: str = ormar.String(max_length=100, unique=True)
    password: str = ormar.String(max_length=128, encrypt_secret=SECRET_KEY, encrypt_backend=ormar.EncryptBackends.HASH)
    is_active: bool = ormar.Boolean(default=False)
