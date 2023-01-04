import re
from fastapi import APIRouter, HTTPException, status, Depends
from models import user, user_login
from db import  engine
from sqlmodel import Session, select
from typing import List
from fastapi.openapi.utils import get_openapi
from passlib.context import CryptContext
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer


api = APIRouter(prefix="/user_ops",tags=["user"])
session  = Session(bind= engine)
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name='user_login'
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



#This block used to custimze the swagger docs
async def custom_openapi():
    if api.openapi_schema:
        return api.openapi_schema
    openapi_schema = get_openapi(
        title="REVERPRO_API",
        version="0.1",
        description="reverpro",
        routes=api.routes,)
    
    api.openapi_schema = openapi_schema
    return api.openapi_schema
api.openapi = custom_openapi


#This block used to get the user details by passing the user id

@api.get("/{user_id}")
async def get_user(user_id: int,  token: str = Depends(reuseable_oauth)):
    result = session.get(user, user_id)
    if not result:
        raise HTTPException(status_code=404, detail= "user not found")
    return {"status":"True","data":[result]}




#This block used to get the all users details 
@api.get('/')
async def get_alluser(token: str = Depends(reuseable_oauth)):
    statement = select(user)
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail="user is not found")
    return {"status": True, "data":[results], "message":"sucess"} 


#This block used to add the new user in the database
@api.post('/users', status_code=status.HTTP_201_CREATED)
async def add_user(users:user):
    statement = select(user).where(user.email_id == users.email_id)
    results = session.exec(statement).all()
    if len(results) == 0:
        result = user.from_orm(users)
        result.created_dt = datetime.now()
        if result.password != None:
            result.password = password_context.hash(result.password)
        session.add(result)
        session.commit()
    else:
        return{"message":"user alredy exit"}
    #session.refresh(result)
    return {"status":True, "message": "New user added"}


#This block used to the update or change the user details
@api.put('/user/{user_id}')
async def update_user(user_id:int, users:user, token: str = Depends(reuseable_oauth)):
    result = session.get(user, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="user not found")
    user_data = users.dict(exclude_unset= True)
    for key, value in user_data.items():
        setattr(result, key, value)
    session.add(result)
    session.commit()
    session.refresh(result)
    return {"status":True,"data":[result], "message":"sucess"}

#THis block code used to delete the user from database
@api.delete('/user/{user_id}')
async def delete_user(user_id: int, token: str = Depends(reuseable_oauth)):
    result = session.get(user, user_id)
    if not result:
        raise HTTPException(status_code = 404, detail="user not found")
    else:
        session.delete(result)
        session.commit()
        return {"Status": True, "message": "sucessfully deleted"}