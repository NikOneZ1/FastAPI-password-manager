from datetime import datetime

from fastapi import Depends, status, HTTPException

from payments.models import MemberAccount
from user.dependencies import get_current_user
from user.models import User


async def check_user_subscription(user: User = Depends(get_current_user)) -> User | bool:
    member_account = await MemberAccount.objects.first(user=user)
    if not member_account.is_member or member_account.membership_end_date < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a member")
    return user
