"""Repositories package module."""

import logging
from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional, List

import sqlalchemy.orm as orm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import func

from app.package.models import Package
from app.release.models import Release

logger = logging.getLogger(__name__)


class PackageRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def package_count(self) -> int:
        async with self.session_factory() as session:
            query = select(func.count(Package.id))
            results = await session.execute(query)
            number_of_packages = results.scalar()

            return number_of_packages

    async def latest_packages(self, limit=5) -> List[Package]:
        async with self.session_factory() as session:
            query = select(Release) \
                .options(
                orm.joinedload(Release.package)) \
                .order_by(Release.created_date.desc()) \
                .limit(limit)

            results = await session.execute(query)
            releases = results.scalars()

            return list({r.package for r in releases})

    async def get_package_by_id(self, package_name: str) -> Optional[Package]:
        async with self.session_factory() as session:
            query = select(Package).filter(Package.id == package_name)
            result = await session.execute(query)
            package = result.scalar_one_or_none()

            return package
