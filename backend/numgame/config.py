from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / "backend.env"
# Settings loading
class Settings(BaseSettings):
    # Database
    database_url:str = ""
    # Server
    server_port:int = 8080
    # Redis Server
    redis_host:str = ""
    redis_port:int = 6379
    redis_password:Optional[str] = None
    # Load .env
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="allow",
    )

settings = Settings()