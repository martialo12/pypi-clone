"""services user module."""

from typing import Optional

from .repositories import UserRepository
from app.user.models import User


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    async def get_user(self, user_id: int) -> Optional[User]:
        user = await self._repository.get_user(user_id)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self._repository.get_user_by_email(email)
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        user = await self._repository.get_user_by_id(user_id)
        return user

    async def user_count(self) -> int:
        number_of_users = await self._repository.user_count()
        return number_of_users
