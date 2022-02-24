from typing import Optional

from dependency_injector.wiring import Provide
from fastapi import Depends
from starlette.requests import Request

from .base_viewmodel import ViewModelBase


class RegisterViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.name = ''
        self.password = ''
        self.email = ''

    async def load(self):
        form = await self.request.form()
        self.name = form.get('name')
        self.password = form.get('password')
        self.email = form.get('email')

        if not self.name or not self.name.strip():
            self.error = "Your name is required."
        elif not self.email or not self.email.strip():
            self.error = "Your email is required."
        elif not self.password or len(self.password) < 5:
            self.error = "Your password is required and must be at 5 characters."
