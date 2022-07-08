from typing import List
from fastapi import APIRouter
from account.models import Account
from account.schemas import RequestAccount

router = APIRouter()


@router.get("/", response_model=List[Account])
async def get_accounts():
    accounts = await Account.objects.all()
    return accounts


@router.post("/", response_model=Account)
async def create_account(account: RequestAccount):
    return await Account(**account.dict()).save()
