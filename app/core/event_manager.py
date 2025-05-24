import inspect
from inspect import Parameter
from contextlib import asynccontextmanager
from typing import Any
from collections.abc import Callable, Coroutine
from asyncio import Queue, iscoroutinefunction
import anyio
import anyio.abc
from loguru import logger
from app.schemas import WsMessage
from app.core.utils import enhanced_isinstance

EventType = WsMessage
HandlerType = Callable[[EventType], Coroutine[Any, Any, Any]]

queue: Queue[EventType] = Queue()
handlers: dict[EventType, list[HandlerType]] = {}

async def publish(e: EventType):
    if enhanced_isinstance(e, EventType):
        logger.debug(f"New event recv. {e}")
        return await queue.put(e)
    logger.error(f"Wrong event type detected when publish. Expect {EventType} but {type(e)}")

async def run_main(tg: anyio.abc.TaskGroup):
    while True:
        e = await queue.get()


@asynccontextmanager
async def lifespan(*_, **__: dict[str, Any]):
    async with anyio.create_task_group() as tg:
        with anyio.CancelScope(shield=True):
            tg.start_soon(run_main, tg)
            yield
            tg.cancel_scope.cancel()

def register(handler: HandlerType):
    if not inspect.isfunction(handler):
        logger.critical("Handler not a function.")
        raise RuntimeError()
    if not iscoroutinefunction(handler):
        logger.critical("Handler not a coroutine function")
        raise RuntimeError()
    # 获取函数签名
    signature = inspect.signature(handler)
    non_default_non_var_params = 0
    for param in signature.parameters.values():
        # 排除可变参数（*args 和 **kwargs）
        if param.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
            continue
        # 检查是否是非默认值参数
        if param.default == Parameter.empty:
            non_default_non_var_params += 1
    # 检查是否只有一个非默认值且非可变参数
    if non_default_non_var_params != 1:
        logger.critical(f"Handler function's parm mismatch. Expect 1 but {non_default_non_var_params}")
        raise RuntimeError()
    annotations = tuple(handler.__annotations__.values())
    if len(annotations) != 1:
        logger.critical(f"Handler function's annotation mismatch. Expect 1 but {len(annotations)}")
        raise RuntimeError()
    event_type = annotations[0]
    if not enhanced_isinstance(event_type, type[EventType]):
        logger.critical(f"Handler with invalid event_type parm. Expect {type[EventType]} but {event_type}")
        raise RuntimeError()
    handlers.setdefault(event_type, []).append(handler)
    return handler