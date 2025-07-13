import secrets

from typing import Annotated
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, BeforeValidator
from app.models import ConfigRoute
from app.core.utils import parse_cors, load_routes_config, load_port_config

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore"
    )
    ROUTES: list[ConfigRoute] = load_routes_config()
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    TOKEN_URL_PATH: str
    TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    # BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
    
    SERVER_PORT: int = load_port_config()
    HOSTNAME: str
    PORT: int
    
    
settings = Settings() # type: ignore