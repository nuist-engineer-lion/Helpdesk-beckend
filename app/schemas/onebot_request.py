from typing import Literal, Any
from pydantic import BaseModel, UUID4

class OneBotRequest(BaseModel):
    action: str
    params: dict[str, Any]
    echo: UUID4

    model_config = {"extra": "ignore"}

class OneBotResponse(BaseModel):
    status: Literal["ok", "failed"]
    retcode: int
    data: Any | None = None
    message: str = ""
    wording: str = ""
    echo: UUID4
    
    model_config = {"extra": "ignore"}