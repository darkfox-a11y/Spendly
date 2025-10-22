import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    # 1. READ THESE FROM YOUR .env FILE
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # 2. SET THE CORRECT HOSTNAME FOR DOCKER
    # This must match your docker-compose.yml service name
    POSTGRES_HOST: str = "spendly_db" 
    POSTGRES_PORT: int = 5432
    
    # This is the correct Pydantic V2 syntax
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    # 3. BUILD THE DATABASE_URL AUTOMATICALLY
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        # This creates the correct URL, e.g.:
        # postgresql://fastapi_user:fastapi_pass@spendly_db:5432/subscription_db
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --- OTHER SETTINGS ---
    PROJECT_NAME: str = "Spendly: AI Subscription Manager"
    JWT_SECRET_KEY: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # NOTE: If your Redis is also a Docker container,
    # you must change 'localhost' to its service name here.
    REDIS_URL: str = "redis://localhost:6379/0" 
    
    GROQ_API_KEY: Optional[str] = None
    APP_ENV: str = "development"
    SMTP_EMAIL: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None


settings = Settings()