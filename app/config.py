import logging
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    VERIFY_SSL: bool = True
    LOG_LEVEL: int = logging.DEBUG
    LOG_FILENAME: str = "/opt/logs/api.log"
    PORT: int = 8080
    HOST: str = "127.0.0.1"

    # Swagger Settings
    SWAGGER_DESCRIPTION: str = "Foo"
    SWAGGER_TITLE: str = "API"
    SWAGGER_PATH: str = f"{os.path.dirname(__file__)}/swagger_files"

    class Config:
        env_prefix = ""


settings = Settings()
