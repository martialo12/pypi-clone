"""Endpoints package module."""

import logging
from typing import Optional

import fastapi
from dependency_injector.wiring import inject, Provide
from fastapi_jinja import template
from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from starlette import status
from starlette.responses import RedirectResponse

from app.containers import Container
from app.user.services import UserService
from app.core.viemodels.details_viewmodel import DetailsViewModel
from app.core.cookies import cookie_auth
from .services import PackageService
from app.release.services import ReleaseService
from app.core.viemodels.index_viewmodel import IndexViewModel


logger = logging.getLogger(__name__)

package = APIRouter(tags=["package"])


@package.get('/home')
@package.get('/')
@inject
@template(template_file="/home/index.html")
async def home(
        request: Request,
        release_service: ReleaseService = Depends(Provide[Container.release_service]),
        user_service: UserService = Depends(Provide[Container.user_service]),
        package_service: PackageService = Depends(Provide[Container.package_service])
) -> Optional[RedirectResponse or dict]:

    user_id = cookie_auth.get_user_id_via_auth_cookie(request)
    logger.debug(f"user id: {user_id}")
    if not user_id:
        resp = fastapi.responses.RedirectResponse("/account/login", status_code=status.HTTP_302_FOUND)
        return resp

    release_count = await release_service.release_count()
    user_count = await user_service.user_count()
    package_count = await package_service.package_count()
    packages = await package_service.latest_packages(limit=7)
    logger.debug(f"release_count: {release_count}")
    logger.debug(f"user_count: {user_count}")
    logger.debug(f"package_count: {package_count}")
    logger.debug(f"packages: {packages}")
    vm = IndexViewModel(request)
    vm.to_dict().update(
        {
            "release_count": release_count,
            "user_count": user_count,
            "package_count": package_count,
            "packages": packages
        }
    )
    return vm.to_dict()


@package.get('/project/{package_name}', include_in_schema=False)
@inject
@template(template_file='/package/details.html')
async def details(
        package_name: str,
        request: Request,
        release_service: ReleaseService = Depends(Provide[Container.release_service]),
        package_service: PackageService = Depends(Provide[Container.package_service])
) -> Optional[RedirectResponse or dict]:

    user_id = cookie_auth.get_user_id_via_auth_cookie(request)
    logger.debug(f"user id: {user_id}")
    if not user_id:
        resp = fastapi.responses.RedirectResponse("/account/login", status_code=status.HTTP_302_FOUND)
        return resp

    logger.info("project endpoint")
    vm = DetailsViewModel(package_name, request)

    package = await package_service.get_package_by_id(package_name)
    latest_release = await release_service.get_latest_release_for_package(package_name)
    latest_version = f'{latest_release.major_ver}.{latest_release.minor_ver}.{latest_release.build_ver}'
    logger.debug(f"package: {package}")
    logger.debug(f"latest_release: {latest_release}")
    logger.debug(f"latest_version: {latest_version}")

    vm.to_dict().update(
        {
            "package": package,
            "latest_release": latest_release,
            "latest_version": latest_version
        }
    )

    return vm.to_dict()
