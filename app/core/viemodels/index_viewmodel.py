"""account viemodel module."""

from typing import List

from starlette.requests import Request

from app.package.models import Package
from app.core.viemodels.base_viewmodel import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.release_count: int = 0
        self.user_count: int = 0
        self.package_count: int = 0
        self.packages: List[Package] = []
