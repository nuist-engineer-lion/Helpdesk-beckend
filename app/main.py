from fastapi import FastAPI
from app.api.v1 import ws
from app.core.event_manager import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(ws.router)