"""Repositories release module."""

import logging
from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional, List

import sqlalchemy.orm as orm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import func

from app.release.models import Release

logger = logging.getLogger(__name__)


class ReleaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def release_count(self) -> int:
        async with self.session_factory() as session:
            query = select(func.count(Release.id))
            results = await session.execute(query)
            number_of_release = results.scalar()

            return number_of_release

    async def get_latest_release_for_package(self, package_name: str) -> Optional[Release]:
        async with self.session_factory() as session:
            query = select(Release) \
                .filter(Release.package_id == package_name) \
                .order_by(Release.created_date.desc())

            results = await session.execute(query)
            release = results.scalar()

            return release
