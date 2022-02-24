"""Endpoints auth module."""
import asyncio
import logging
from typing import Optional

import fastapi.responses
from dependency_injector.wiring import inject, Provide
from fastapi_jinja import template
from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
)
from starlette.responses import RedirectResponse

from app.containers import Container
from app.core.cookies import cookie_auth
from app.user.services import UserService
from .services import AuthService
from app.core.viemodels.login_viewmodel import LoginViewModel
from app.core.viemodels.register_viewmodel import RegisterViewModel
from app.user.schemas import (
    UserLogin,
    UserCreate
)

logger = logging.getLogger(__name__)

auth = APIRouter(tags=["authentication"])


@auth.get("/account/login")
@template(template_file="/auth/login.html")
async def login_get(request: Request) -> Optional[RedirectResponse or dict]:
    user_id = cookie_auth.get_user_id_via_auth_cookie(request)
    logger.debug(f"user id: {user_id}")
    if user_id:
        resp = fastapi.responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        return resp
    vm = LoginViewModel(request)
    logger.debug(f"vm login: {vm.to_dict()}")
    return vm.to_dict()


@auth.post("/account/login")
@inject
@template(template_file="/auth/login.html")
async def login_post(
        request: Request,
        auth_service: AuthService = Depends(Provide[Container.auth_service])
) -> Optional[RedirectResponse, dict]:
    vm = LoginViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    user_login = UserLogin(email=vm.email, password=vm.password)
    logger.debug(f"user_login: {user_login}")
    user = await auth_service.login_user(user_login)
    logger.debug(f"user: {user}")
    if not user:
        await asyncio.sleep(5)
        vm.error = "The account does not exist or the password is wrong."
        return vm.to_dict()

    resp = fastapi.responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(resp, user.id)
    logger.debug(f"resp: {resp}")
    return resp


@auth.get('/account/register')
@template(template_file="/auth/register.html")
def register_get(request: Request) -> Optional[RedirectResponse, dict]:
    user_id = cookie_auth.get_user_id_via_auth_cookie(request)
    logger.debug(f"user id: {user_id}")
    if user_id:
        resp = fastapi.responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        return resp
    vm = RegisterViewModel(request)
    logger.info(f"vm : {vm.to_dict()}")
    return vm.to_dict()


@auth.post('/account/register')
@inject
@template(template_file="/auth/register.html")
async def register_post(
        request: Request,
        user_service: UserService = Depends(Provide[Container.user_service]),
        auth_service: AuthService = Depends(Provide[Container.auth_service])
) -> Optional[RedirectResponse, dict]:
    vm = RegisterViewModel(request)
    await vm.load()
    logger.debug(f"vm: {vm.to_dict()}")

    logger.debug(f"email: {vm.email}")
    user = await user_service.get_user_by_email(vm.email)
    logger.debug(f"user: {user}")
    if user is not None:
        vm.error = "That email is already taken. Log in instead?"

    if vm.error is not None:
        return vm.to_dict()

    # Create the account
    user_create = UserCreate(email=vm.email, name=vm.name, password=vm.password)
    account = await auth_service.create_account(user_create)

    logger.debug(f"account: {account}")

    # Login user
    resp = fastapi.responses.RedirectResponse(url='/account', status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(resp, account.id)

    return resp


@auth.get('/account/logout', include_in_schema=False)
def logout() -> RedirectResponse:
    response = fastapi.responses.RedirectResponse(url='/account/login', status_code=status.HTTP_302_FOUND)
    cookie_auth.logout(response)

    return response
