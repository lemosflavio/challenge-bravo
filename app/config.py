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
    SWAGGER_DESCRIPTION: str = "Conversion between currencies"
    SWAGGER_TITLE: str = "EXCHANGE API"
    SWAGGER_PATH: str = f"{os.path.dirname(__file__)}/swagger_files"

    # Mongo Settings
    MONGO_USER: str = ""
    MONGO_PASSWORD: str = ""
    MONGO_HOST: str = "localhost"
    MONGO_DB: str = "exchange"

    # Mongo Collections
    MONGO_EXCHANGE_TAX_COLLECTION: str = "exchange_tax"

    class Config:
        env_prefix = ""

    @property
    def mongo_uri(self) -> str:
        if not self.MONGO_USER and not self.MONGO_PASSWORD:
            return f"mongodb://{self.MONGO_HOST}/{self.MONGO_DB}"
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}/{self.MONGO_DB}"


settings = Settings()
