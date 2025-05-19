from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import WebsocketUrl
from loguru import logger

class Settings(BaseSettings):
    ws_url: WebsocketUrl = WebsocketUrl('ws://192.168.33.1')
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

@lru_cache
def get_settings():
    logger.debug("Getting new settings instance...")
    settings = Settings()
    return settings

print(get_settings())