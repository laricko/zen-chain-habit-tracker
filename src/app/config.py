from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    telegram_bot_token: str

    @property
    def pg_dsn(self) -> PostgresDsn:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@localhost:5432/{self.postgres_db}"


config = Config()
