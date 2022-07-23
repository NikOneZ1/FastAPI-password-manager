from typing import List
from fastapi import APIRouter, status
from fastapi.params import Depends

from account.models import Account
from account.schemas import RequestAccount, AccountListResponseSchema, AccountResponseSchema
from payments.dependencies import check_user_subscription
from user.dependencies import get_current_user
from user.models import User

router = APIRouter()


@router.get("/", response_model=List[AccountListResponseSchema])
async def get_accounts(user: User = Depends(get_current_user)):
    accounts = await Account.objects.select_related(Account.user).all(user=user)
    return accounts


@router.post("/", response_model=AccountResponseSchema)
async def create_account(account: RequestAccount, user: User = Depends(check_user_subscription)):
    return await Account(**account.dict(), user=user).save()


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_id: int, user: User = Depends(get_current_user)):
    await Account.objects.filter(id=account_id, user=user).delete()
    return True
