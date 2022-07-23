from typing import Dict, Union, Optional

import ormar

from core.db import BaseMeta
from core.settings import SECRET_KEY
from user.models import User


class Account(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'accounts'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)
    login: str = ormar.String(max_length=100)
    password: str = ormar.String(max_length=100, encrypt_secret=SECRET_KEY,
                                 encrypt_backend=ormar.EncryptBackends.FERNET)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, backref='accounts', nullable=False)
