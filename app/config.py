from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://app:app@db:5432/app"
    jwt_secret: str = "devsupersecret"
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60
    redis_url: str = "redis://redis:6379/0"
    rabbit_url: str = "amqp://guest:guest@rabbitmq:5672/"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
