from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from core.settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from mail.tasks import send_activation_mail_task
from user.dependencies import get_current_user, refresh, get_user_by_email_token
from user.models import User
from user.schemas import Token, CreateUser, UserResponse
from user.utils import authenticate_user, create_access_token, create_refresh_token

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(user: CreateUser, background_tasks: BackgroundTasks):
    created_user = await User(**user.dict()).save()
    background_tasks.add_task(send_activation_mail_task, created_user)
    return created_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token,  "token_type": "bearer"}


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_access_token(tokens: tuple[str, str] = Depends(refresh)):
    return Token(access_token=tokens[0], refresh_token=tokens[1], token_type="bearer")


@router.get("/activate/{token}", response_model=UserResponse)
async def activate_user(user: User = Depends(get_user_by_email_token)):
    await user.update(is_active=True)
    return user

