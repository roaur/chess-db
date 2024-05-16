from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn

settings = Settings()
