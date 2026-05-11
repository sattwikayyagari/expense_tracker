from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated, Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str,Field(min_length=8, description='Enter the password')]

class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str,Field(min_length=8, description='Enter the password')]

class UserUpdate(BaseModel):
    email: Optional[EmailStr]= None
    password: Annotated[Optional[str],Field(min_length=8, description='Enter the password')]=None

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config= ConfigDict(from_attributes=True)