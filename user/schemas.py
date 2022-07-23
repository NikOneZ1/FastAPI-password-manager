from pydantic import BaseModel

from user.models import User


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


CreateUser = User.get_pydantic(exclude={"id", "accounts"})
UserResponse = User.get_pydantic(exclude={"accounts"})
