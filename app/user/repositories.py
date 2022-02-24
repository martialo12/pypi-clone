"""Repositories auth module."""
""
import logging
from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import func

from app.user.models import User

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_user(self, user_id: int) -> Optional[User]:
        async with self.session_factory() as session:
            query = select(User).filter(User.id == user_id)
            result = await session.execute(query)

            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self.session_factory() as session:
            query = select(User).filter(User.email == email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if not user:
                return None
                # raise HTTPException(status_code=404, detail="User not found")

            return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        async with self.session_factory() as session:
            query = select(User).filter(User.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            return user

    async def user_count(self) -> int:
        async with self.session_factory() as session:
            query = select(func.count(User.id))
            result = await session.execute(query)
            number_of_user = result.scalar()

            return number_of_user
