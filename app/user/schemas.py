"""schemas user module."""

from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    is_active: Optional[bool] = True


class UserOut(UserBase):
    pass


class UserLogin(UserBase):
    password: str


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: Optional[str]
    token_type: Optional[str]


class TokenData(BaseModel):
    email: Optional[str] = None
