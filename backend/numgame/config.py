from pydantic_settings import BaseSettings, SettingsConfigDict

# Settings loading
class Settings(BaseSettings):
    # Database
    database_url:str = ""
    # Server
    server_port:int = 8080
    # Load .env
    model_config = SettingsConfigDict(
        env_file="../backend.env",
        env_file_encoding="utf-8",
        extra="allow",
    )

settings = Settings()