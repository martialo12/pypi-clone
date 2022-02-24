"""services package module."""

from typing import Optional, List

from .repositories import PackageRepository
from app.package.models import Package


class PackageService:
    def __init__(self, package_repository: PackageRepository) -> None:
        self._repository: PackageRepository = package_repository

    async def package_count(self) -> int:
        number_of_packages = await self._repository.package_count()
        return number_of_packages

    async def latest_packages(self, limit=5) -> List[Package]:
        packages = await self._repository.latest_packages(limit)
        return packages

    async def get_package_by_id(self, package_name: str) -> Optional[Package]:
        package = await self._repository.get_package_by_id(package_name)
        return package
