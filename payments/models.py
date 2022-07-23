from datetime import datetime
from typing import Optional, Union, Dict

import ormar
from ormar import post_save

from core.db import BaseMeta
from user.models import User


class MemberAccount(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'member_account'

    id: int = ormar.Integer(primary_key=True)
    customer_id: str = ormar.String(max_length=100, nullable=True)
    subscription_id: str = ormar.String(max_length=100, nullable=True)
    is_member: bool = ormar.Boolean(default=False)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, backref='member_accounts', nullable=False)
    membership_end_date: datetime = ormar.DateTime(nullable=True)


@post_save(User)
async def create_member_account(sender, instance, **kwargs):
    await MemberAccount.objects.create(user=instance)
