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
    game_management_hashtable:str = "GameManagement"
    # Frontend setting
    frontend_url:str = ""
    # Util setting
    names_csv:str = "names_and_connotations.csv"
    # Load .env
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="allow",
    )

settings = Settings()