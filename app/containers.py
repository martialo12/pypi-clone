"""Containers module."""

import logging

from dependency_injector import containers, providers

from app.db.database import Database
from app.user.services import UserService
from app.auth.services import AuthService
from app.package.services import PackageService
from app.release.services import ReleaseService
from app.user.repositories import UserRepository
from app.auth.repositories import AuthRepository
from app.package.repositories import PackageRepository
from app.release.repositories import ReleaseRepository


logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger.debug(f"config url db: {config.services.app.environment.SQLITE_URL}")
    db = providers.Singleton(Database, db_url=config.services.app.environment.SQLITE_URL)

    # user
    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )

    # auth
    auth_repository = providers.Factory(
        AuthRepository,
        session_factory=db.provided.session
    )

    auth_service = providers.Factory(
        AuthService,
        auth_repository=auth_repository
    )

    # package
    package_repository = providers.Factory(
        PackageRepository,
        session_factory=db.provided.session
    )

    package_service = providers.Factory(
        PackageService,
        package_repository=package_repository
    )

    # release
    release_repository = providers.Factory(
        ReleaseRepository,
        session_factory=db.provided.session
    )

    release_service = providers.Factory(
        ReleaseService,
        release_repository=release_repository
    )
