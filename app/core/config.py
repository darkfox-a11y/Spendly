from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Spendly: AI Subscription Manager"
    DATABASE_URL: str = "postgresql://fastapi_user:fastapi_pass@localhost:5432/subscription_db"
    JWT_SECRET_KEY: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = "demo-API_KEY"
    APP_ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
