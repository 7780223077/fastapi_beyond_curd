import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreateModel(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str


class UserOut(BaseModel):
    uid: uuid.UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str