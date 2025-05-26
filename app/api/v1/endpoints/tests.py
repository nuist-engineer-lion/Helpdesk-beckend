from fastapi import APIRouter
from app.onebot.api import send_private_msg
from app.schemas.qq import TextMessageSegment, TextData

router = APIRouter(prefix="/tests")

@router.get("/")
async def test():
    return await send_private_msg(3892215616, user_id=5079132, message=[TextMessageSegment(data=TextData(text="hahaha"))])