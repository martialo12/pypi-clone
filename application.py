"""Application module."""

import os
import logging.config

import fastapi_jinja
import asyncio
import nest_asyncio
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
import uvicorn

from app.containers import Container
from app.auth import endpoints as auth_endpoints
from app.user import endpoints as user_endpoints
from app.package import endpoints as package_endpoints
from app.core import config

logging.config.fileConfig(os.path.join(os.getcwd(), "app/core/logging.ini"), disable_existing_loggers=True)

# create logger
logger = logging.getLogger('pypi-clone')

nest_asyncio.apply()

pypi_app = FastAPI(title=config.PROJECT_NAME)


async def create_app() -> None:
    await configure()
    uvicorn.run(pypi_app, host="127.0.0.1", port=8000, debug=True)


async def configure(dev_mode=True) -> None:
    container = configure_container()
    await configure_db_container(container)
    pypi_app.container = container
    configure_routes()
    configure_templates(dev_mode)


def configure_container() -> Container:
    container = Container()
    container.config.from_yaml(config.CONFIG_FILE)
    container.wire(modules=[package_endpoints, auth_endpoints, user_endpoints])

    return container


async def configure_db_container(container: Container) -> None:
    db = container.db()
    await db.create_database()


def configure_routes() -> None:
    script_dir = os.path.dirname(__file__)
    st_abs_file_path = os.path.join(script_dir, "app/static/")
    pypi_app.mount('/static', StaticFiles(directory=st_abs_file_path), name='static')
    pypi_app.include_router(package_endpoints.package)
    pypi_app.include_router(auth_endpoints.auth)
    pypi_app.include_router(user_endpoints.user)


def configure_templates(dev_mode: bool) -> None:
    current_folder = os.path.dirname(__file__)
    template_folder = os.path.join(current_folder, 'app/templates')
    template_folder = os.path.abspath(template_folder)
    print(f"template folder: {template_folder}")
    fastapi_jinja.global_init(template_folder, auto_reload=dev_mode)


if __name__ == '__main__':
    asyncio.run(create_app())
else:
    asyncio.run(configure())
