from typing import TypedDict, Unpack
from app.core.request_manager import send_request
from app.schemas.qq import MessageSegment

class PrivateMsgParam(TypedDict):
    user_id: int
    message: list[MessageSegment]

async def send_private_msg(bot_id: int, timeout: float = 30.0, **params: Unpack[PrivateMsgParam]):
    return await send_request(bot_id, "send_private_msg", dict(params), timeout)