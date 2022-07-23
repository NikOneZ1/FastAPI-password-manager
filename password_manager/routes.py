from fastapi import APIRouter
from account import views as account_views
from user import views as user_views
from payments import views as payments_views

routes = APIRouter()

routes.include_router(account_views.router, prefix="/account", tags=["account"])
routes.include_router(user_views.router, prefix="/user", tags=["user"])
routes.include_router(payments_views.router, prefix="/payments", tags=["payments"])
