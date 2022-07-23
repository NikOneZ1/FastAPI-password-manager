from pydantic import BaseModel

from user.schemas import UserResponse


class RequestAccount(BaseModel):
    class Config:
        orm_mode = True

    name: str
    login: str
    password: str


class AccountListResponseSchema(RequestAccount):
    id: int


class AccountResponseSchema(AccountListResponseSchema):
    user: UserResponse

