import os

# configuration
PROJECT_NAME = os.environ.get("PROJECT_NAME", "pypi_clone")
AUTH_COOKIE_NAME = os.environ.get("AUTH_COOKIE_NAME", "pypi_account")
CONFIG_FILE = "docker-compose.yml"
