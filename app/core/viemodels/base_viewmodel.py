from typing import Optional

from starlette.requests import Request

from app.core.cookies.cookie_auth import get_user_id_via_auth_cookie


class ViewModelBase:

    def __init__(self, request: Request):
        self.request: Request = request
        self.error: Optional[str] = None
        self.user_id: Optional[int] = get_user_id_via_auth_cookie(self.request)

        # We'll get this once we have users from the cookies
        self.is_logged_in = self.user_id is not None

    def to_dict(self) -> dict:
        return self.__dict__
