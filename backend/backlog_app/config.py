import logging
from pathlib import Path
from typing import Literal

from pydantic import AmqpDsn, BaseModel, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent


class LoggingConfig(BaseModel):
    log_format: str = (
        "[-] %(asctime)s [%(levelname)s] %(module)s-%(lineno)d - %(message)s"
    )
    worker_log_format: str = (
        "[-] %(asctime)s [%(levelname)s] [%(processName)s] %(module)s-%(lineno)d - %(message)s"
    )
    log_level_name: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "WARNING"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class SuperUser(BaseModel):
    email: str
    password: str


class DataBaseConnection(BaseModel):
    host: str
    port: int
    username: str
    password: str
    name: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class DataBase(BaseModel):
    connection: DataBaseConnection


class TaskiqConfig(BaseModel):
    rbmq_host: str
    rbmq_port: int
    rbmq_username: str
    rbmq_password: str

    @property
    def url(self) -> str:
        return f"amqp://{self.rbmq_username}:{self.rbmq_password}@{self.rbmq_host}:{self.rbmq_port}//"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(
            ROOT_DIR / ".env.template",
            ROOT_DIR / ".env",
        ),
        env_prefix="BACKLOG__",
        env_nested_delimiter="__",
        yaml_file=(
            ROOT_DIR / "config.default.yaml",
            ROOT_DIR / "config.local.yaml",
        ),
        yaml_config_section="backlog",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources and their order for loading the settings values.
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )

    db: DataBase
    taskiq: TaskiqConfig
    logging: LoggingConfig = LoggingConfig()
    access_token_db: AccessToken
    superuser: SuperUser
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
