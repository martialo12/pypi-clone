"""services release module."""

from typing import Optional

from .repositories import ReleaseRepository
from app.release.models import Release


class ReleaseService:
    def __init__(self, release_repository: ReleaseRepository) -> None:
        self._repository: ReleaseRepository = release_repository

    async def release_count(self) -> int:
        number_of_releases = await self._repository.release_count()
        return number_of_releases

    async def get_latest_release_for_package(self, package_name: str) -> Optional[Release]:
        release = await self._repository.get_latest_release_for_package(package_name)
        return release
