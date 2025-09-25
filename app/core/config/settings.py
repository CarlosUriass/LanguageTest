from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Main application settings."""
    # App settings
    APP_NAME: str = "Language Test API"
    DEBUG: bool = False
    
    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    # LLM settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        """Get PostgreSQL connection URL."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def redis_url(self) -> str:
        """Get Redis connection URL."""
        password = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{password}{self.REDIS_HOST}:{self.REDIS_PORT}/0"


# Global settings instance
settings = Settings()