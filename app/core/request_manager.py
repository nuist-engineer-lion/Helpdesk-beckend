import uuid
from typing import Any
from asyncio import Future
from app.schemas.onebot_request import OneBotResponse, OneBotRequest
from app.core.event_manager import register
from app.api.v1.ws import manager
from loguru import logger
import anyio

pending_requests: dict[uuid.UUID, Future[OneBotResponse]] = {}

def generate_uuid():
    while((v:=uuid.uuid4()) in pending_requests):
        logger.warning("Duplicate uuid detect!")
    return v

async def send_request(bot_id: int, action: str, params: dict[str, Any], timeout: float = 30.0) -> OneBotResponse | None:
    """发送请求并异步等待响应"""
    echo = generate_uuid()
    future: Future[OneBotResponse] = Future()
    pending_requests[echo] = future
    response = None

    request_data = OneBotRequest(action=action, params=params, echo=echo)

    async with anyio.create_task_group():
        with anyio.move_on_after(timeout):
            success = await manager.send_message(bot_id, request_data.model_dump_json())
            if success:
                response = await future

    pending_requests.pop(echo, None)
    return response

@register
async def handle_response(e: OneBotResponse):
    """处理接收到的响应消息"""
    if e.echo and e.echo in pending_requests:
        future = pending_requests[e.echo]
        if not future.done():
            future.set_result(e)
            logger.debug(f"Response matched for echo {e.echo}")
        else:
            logger.warning(f"Unmatched response with echo {e.echo}")