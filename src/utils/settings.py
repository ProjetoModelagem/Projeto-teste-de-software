from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "projeto_biblioteca"
    database_url: str = "sqlite:///./library_db.sqlite3"
    log_level: str = "INFO"
    reports_dir: str = "./reports"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> 'Settings':
    return Settings()