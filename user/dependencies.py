from datetime import timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from redis.client import Redis

from core.settings import *
from user.models import User
from user.schemas import TokenData
from user.utils import get_user,  create_access_token, create_refresh_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

redis_conn = Redis(host='redis', port=6379, db=0, decode_responses=True)


async def get_user_by_token(token: str) -> tuple[User, str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user, token


async def get_user_by_email_token(token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = await User.objects.get(email=email)
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user, token = await get_user_by_token(token)
    return user


async def refresh(user: get_user_by_token = Depends()) -> tuple[str, str]:
    user, token = user
    if redis_conn.get(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    redis_conn.setex(token, REFRESH_TOKEN_EXPIRE_MINUTES, "true")
    return access_token, refresh_token
