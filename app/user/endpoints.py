"""Endpoints user module."""
import asyncio
import logging

import fastapi.responses
from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jinja import template
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    Response
)

from app.containers import Container
from app.core.viemodels.account_viewmodel import AccountViewModel
from .services import UserService

logger = logging.getLogger(__name__)

user = APIRouter(tags=["user"])


@user.get('/account')
@inject
@template(template_file="/home/account.html")
async def account(
        request: Request,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    vm = AccountViewModel(request)
    user_id = vm.user_id
    logger.debug(f"user_id: {user_id}")
    user = await user_service.get_user_by_id(user_id)
    logger.debug(f"user: {user}")
    if user:
        vm.to_dict().update({"user": user})
        return vm.to_dict()

