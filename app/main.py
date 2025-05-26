from fastapi import FastAPI
from app.api.v1 import ws
from app.api.v1.endpoints import tests
from app.core.event_manager import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(ws.router)
app.include_router(tests.router)