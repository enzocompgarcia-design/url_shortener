from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Config(BaseSettings):
    CASSANDRA_HOST: str
    CASSANDRA_PORT: int
    CASSANDRA_TTL_10_YEARS: int = 10 * 365 * 24 * 60 * 60

    REDIS_URL: str

    SECRET_KEY: str
    ALPHABET: str

    NAME_CACHE_ID: str
    ID_START: int

    ORIGINS: list[str]
    ALLOWED_PROTOCOLS: list[str] = ["http", "https"]
    DEFAULT_PROTOCOL: str = "https"

    RATE_LIMIT_WRITE: str = "10/minute"
    RATE_LIMIT_READ: str = "120/minute"

    CACHE_CHECK_TIMEOUT: float = 2.0
    DATABASE_CHECK_TIMEOUT: float = 2.0

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
    )


config = Config()
