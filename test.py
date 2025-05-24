from loguru import logger
from pydantic import BaseModel

class Z(BaseModel):
    t: int = 1

logger.debug(f"sss{Z()}")