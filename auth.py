from fastapi import APIRouter
from models import sgin
from passlib.context import CryptContext


auth_api = APIRouter()


@auth_api.get("/sign")
async def sign():
    pass