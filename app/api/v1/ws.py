from typing import Any
from json import JSONDecodeError
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from anyio import create_task_group, move_on_after
from loguru import logger
from pydantic import ValidationError
# from app.core.config import get_settings, Settings
from app.schemas.qq import WsMessageModel, ConnectEvent

router = APIRouter(prefix='/ws')

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> None | int:
        logger.debug("Receiving a new ws connection...")
        await websocket.accept()
        connect_event_data: dict[str, Any] | None = None
        try:
            logger.debug("Waiting for the connect meta event message...")
            async with create_task_group() as _:
                with move_on_after(1) as scope:
                    connect_event_data = await websocket.receive_json()
                if(scope.cancelled_caught):
                    logger.warning("New Ws Connection Timeout after 1 sec no initial message!")
                    return
        except JSONDecodeError:
            logger.warning("The new ws connection sending non-json initial message...")
            await websocket.close()
            return
        except WebSocketDisconnect:
            logger.warning("The new ws connection closed by client before handshake.")
            return
        try:
            connect_event = WsMessageModel.validate_python(connect_event_data)
        except ValidationError:
            logger.warning("The new ws connection sent a json initial message, but not a WsMessage.")
            await websocket.close()
            return
        if not isinstance(connect_event, ConnectEvent):
            logger.warning("The new ws connection sent first WsMessage, but not a ConnectEvent Message.")
        bot_id = connect_event.self_id
        logger.info(f"A new bot({bot_id}) connected!")
        self.active_connections[bot_id] = websocket
        return bot_id

    async def disconnect(self, bot_id: int):
        if ws:=self.active_connections.pop(bot_id, None):
            logger.info(f"Bot({bot_id}) disconnect successfully!")
            try:
                await ws.close()
            except:
                pass
        else:
            logger.warning(f"Bot({bot_id}) already removed!")

    async def send_message(self, bot_id: int, message: str):
        if bot_id in self.active_connections:
            websocket = self.active_connections[bot_id]
            logger.info(f"Sending message to bot({bot_id})...")
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                logger.error(f"Sending failed. Bot({bot_id}) has been inactive.")
                await self.disconnect(bot_id)
                return False
            logger.info(f"Sending successfully!")
            return True
        else:
            logger.error(f"Sending fail to a non-exist bot({bot_id}).")
            return False
            

    async def broadcast(self, message: str):
        logger.info("Broadcasting message...")
        result = True
        for bot_id in tuple(self.active_connections.keys()):
            result = result and await self.send_message(bot_id, message)
        logger.info("Broadcast done.")
        return result
    
manager = ConnectionManager()

@router.websocket('/')
async def ws_endpoint(websocket: WebSocket):
    bot_id = await manager.connect(websocket)
    if not bot_id:
        return
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(data)
    except WebSocketDisconnect:
        await manager.disconnect(bot_id)