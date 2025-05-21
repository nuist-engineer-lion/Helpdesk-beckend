from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

class Settings(BaseSettings):
    ws_token: str = ''
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

@lru_cache
def get_settings():
    logger.debug("Getting new settings instance...")
    settings = Settings()
    return settings