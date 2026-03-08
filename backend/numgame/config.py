from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional
import os

# Env selection between test env and real env
def select_env():
    suffix = os.getenv('ENV_FILE_PATH')
    if suffix:
        return f"backend.env{suffix}"
    else:
        return "backend.env"

# Directory processing
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / select_env()

# Settings loading
class Settings(BaseSettings):
    # Database
    database_url: str = ""
    sync_database_url: str = ""
    # Server
    server_port: int = 8080
    # Redis Server
    redis_host: str = ""
    redis_port: int = 6379
    redis_password: Optional[str] = None
    game_management_hashtable: str = "GameManagement"
    # Frontend setting
    frontend_url: str = ""
    # Util setting
    names_csv: str = "names_and_connotations.csv"
    # Bot config
    simple_bot_name: str = "<bot>"
    # Load .env
    model_config = SettingsConfigDict(
        env_file = ENV_FILE_PATH,
        env_file_encoding = "utf-8",
        extra = "allow",
    )

settings = Settings()
