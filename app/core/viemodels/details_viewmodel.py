""" details viewmodel module."""

from typing import Optional

from starlette.requests import Request

from app.package.models import Package
from app.release.models import Release
from app.core.viemodels.base_viewmodel import ViewModelBase


class DetailsViewModel(ViewModelBase):
    def __init__(self, package_name: str, request: Request):
        super().__init__(request)

        self.package_name = package_name
        self.latest_version = "0.0.0"
        self.is_latest = True
        self.maintainers = []
        self.package: Optional[Package] = None
        self.latest_release: Optional[Release] = None
