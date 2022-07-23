import base64
import hashlib
from datetime import datetime, timedelta

from jose import jwt

from core.settings import SECRET_KEY, ALGORITHM
from user.models import User


def validate_password(plain_password: str, hashed_password: str) -> bool:
    secret = hashlib.sha256(SECRET_KEY.encode()).digest()
    secret = base64.urlsafe_b64encode(secret)
    hashed = hashlib.sha512(secret + plain_password.encode()).hexdigest()
    return hashed == hashed_password


async def authenticate_user(username: str, password: str) -> User | bool:
    user = await User.objects.get(username=username)
    if not user:
        return False
    if not validate_password(password, user.password):
        return False
    return user


async def get_user(username: str):
    return await User.objects.get(username=username)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=7*24*60)
    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt
