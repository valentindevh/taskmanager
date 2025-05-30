from pydantic_settings import BaseSettings

from pydantic import PostgresDsn # PostgresDsn is likely still in pydantic core

class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql+asyncpg://anatoli:password@host:5432/taskdb'
    APP_ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()