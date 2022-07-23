from datetime import datetime, timedelta

from jose import jwt

from core.settings import BASE_URL, SECRET_KEY, ALGORITHM
from mail.utils import send_sendgrid_mail
from user.models import User


def send_activation_mail_task(user: User):
    to_encode = {"sub": user.email}
    expires_delta = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expires_delta})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    send_sendgrid_mail([user.email], 'Activate your account',
                       f'<h1>Activate your account</h1><a href="{BASE_URL}/user/activate/{token}/">activate</a>')
