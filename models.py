from sqlmodel import  SQLModel, Field
from typing import Optional
from datetime import datetime, date, time
from pydantic import EmailStr, constr, validator
from fastapi import Query
import re, enum


#This block used to create validation for gender
class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NOT_PREFFERD = "NOT_PREFFERD"



#This block used as the schema for sigin endpoint
class user_login(SQLModel):
    email_id: EmailStr
    password: str

#This block used as create the model for the database
class user(SQLModel, table=True): 
    user_id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str]
    first_name:str 
    middle_name:Optional[str]
    last_name:Optional[str]
    doc_number:Optional[str] 
    dob:Optional[str] =  None
    email_id: EmailStr
    phone_no: Optional[str] = None
    created_dt: Optional[datetime]
    gender: Optional[Gender]= Gender.NOT_PREFFERD 
    user_name:Optional[str]
    password:Optional[str]
    password_hint:Optional[str]
    secret_question:Optional[str]
    secret_question_ans:Optional[str]
    phone_no:Optional[str] 
    department:Optional[str]
    address_line1:Optional[str]
    address_line2:Optional[str]
    city:Optional[str]
    state:Optional[str]
    postal_code:Optional[str]
    country_code:Optional[str]
    @validator("phone_no")
    def phone_validation(cls, v):
        regex = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
        if v and not re.search(regex, v, re.I):
            print(v)
            raise ValueError("Phone Number Invalid.")
        return v
    @validator("dob")
    def date_validation(cls, v):
        if v is None:
            pass
        else:
            datetime.strptime(v, '%Y-%m-%d')
            return v
            raise ValueError("dob is invalid")

