from typing import List
from fastapi import APIRouter
from account.models import Account

router = APIRouter()


@router.get("/", response_model=List[Account])
async def get_accounts():
    accounts = await Account.objects.all()
    return accounts
