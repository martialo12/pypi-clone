"""services auth module."""

from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .repositories import AuthRepository
from app.user.models import User
from app.user.schemas import (
    UserBase,
    UserOut,
    UserEdit,
    UserLogin,
    UserCreate,
    TokenData
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")


class AuthService:
    def __init__(self, auth_repository: AuthRepository) -> None:
        self._repository: AuthRepository = auth_repository

    async def login_user(self, user_login: UserLogin) -> Optional[User]:
        user = await self._repository.login_user(user_login)
        return user

    async def create_account(self, user_create: UserCreate) -> Optional[User]:
        user = await self._repository.create_account(user_create)
        return user

    async def get_current_user(self, token: str = Depends(oauth2_schema)) -> Optional[User]:
        user = await self._repository.get_current_user(token)
        return user

    async def get_current_active_user(self, current_user: User = Depends(get_current_user)) -> User:
        user = await self._repository.get_current_active_user(current_user)
        return user



