from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import ws

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

app = FastAPI()
app.include_router(ws.router)