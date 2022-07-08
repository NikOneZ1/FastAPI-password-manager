from fastapi import APIRouter
from account import views

routes = APIRouter()

routes.include_router(views.router, prefix="/account")
