from hashlib import algorithms_guaranteed
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import user_login, user
from passlib.context import CryptContext
from db import  engine
from sqlmodel import Session, select
from jose import  jwt
from utlits import hased

session  = Session(bind= engine)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


auth= APIRouter(prefix="/auth", tags=["Authenticator"])

@auth.post("/login")
def login(cerd: OAuth2PasswordRequestForm = Depends()):
    statement = select(user).filter(user.email_id == cerd.username)
    results = session.exec(statement).first()
    if not results:
        raise HTTPException(status_code=404, detail='user not found')
    hased_password = hased.get_hashed_password(cerd.password)
    pass_valid = hased.verify_password(cerd.password, hased_password)
    if pass_valid is False:
        raise HTTPException(status_code=401, detail = 'username or email not match')
    data = {"sub":results.email_id, "user_id": results.user_id}
    token = jwt.encode(data, "secret_key", algorithm='HS256')
    return {"status":True, "data":[{"acess_token":token}]}


    