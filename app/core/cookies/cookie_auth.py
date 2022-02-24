"""cookie authentication module."""
import hashlib
import logging
from typing import Optional

from fastapi import (
    Request,
    Response
)

from app.core import config


logger = logging.getLogger(__name__)

auth_cookie_name = config.AUTH_COOKIE_NAME


def set_auth(response: Response, user_id: int) -> None:
    hash_user_id = __hash_text(str(user_id))
    val = f"{user_id}:{hash_user_id}"
    response.set_cookie(auth_cookie_name, val, secure=False, httponly=True, samesite='Lax')


def __hash_text(text: str) -> str:
    text = '_salty__' + text + '__text'
    return hashlib.sha512(text.encode('utf-8')).hexdigest()


def get_user_id_via_auth_cookie(request: Request) -> Optional[int]:
    if auth_cookie_name not in request.cookies:
        return None

    val = request.cookies[auth_cookie_name]
    parts = val.split(":")
    if len(parts) != 2:
        return None

    user_id = parts[0]
    hash_user_id = parts[1]
    hash_user_id_check = __hash_text(user_id)

    if hash_user_id != hash_user_id_check:
        logger.warning("Hash mismatch, invalid cookie value")
        return None

    return int(user_id)


def logout(response: Response) -> None:
    response.delete_cookie(auth_cookie_name)
