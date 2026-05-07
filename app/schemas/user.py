from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str,Field(min_length=8, description='Enter the password')]

class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str,Field(min_length=8, description='Enter the password')]

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config= ConfigDict(from_attributes=True)