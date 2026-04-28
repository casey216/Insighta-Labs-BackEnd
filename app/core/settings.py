import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


def _get_env_file() -> str:
    if os.environ.get("TESTING") == "1":
        return "tests/.env.test"
    return ".env"


class Settings(BaseSettings):
    """Class to hold application's config values"""

    model_config = SettingsConfigDict(
        env_file=_get_env_file(),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Environment variables
    ENV: str = "develoment"
    TESTING: bool = False

    # Database variables
    DB_HOST: str = ""
    DB_PORT: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    DB_TYPE: str = ""

    # Github Secrets
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""

    # JWT
    JWT_SECRET_KEY: str


settings = Settings()   # type: ignore
