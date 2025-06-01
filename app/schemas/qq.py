from typing import Literal, Annotated
from pydantic import BaseModel, Field, field_validator, AnyHttpUrl, TypeAdapter
from datetime import datetime

class OneBotEventBase(BaseModel):
    time: int
    self_id: int

    model_config = {"extra": "ignore"}
    
    @field_validator('time')
    @classmethod
    def validate_timestamp(cls, v: int) -> int:
        # 验证时间戳是否合理（大于0且不超过当前时间太多）
        current_time = int(datetime.now().timestamp())
        if v <= 0:
            raise ValueError("时间戳必须大于0")
        if v > current_time + 86400:  # 不超过当前时间一天
            raise ValueError("时间戳不能超过当前时间太多")
        return v

class MetaEventBase(OneBotEventBase):
    post_type: Literal['meta_event'] = 'meta_event'

class LifecycleMetaEventBase(MetaEventBase):
    meta_event_type: Literal['lifecycle'] = 'lifecycle'

class ConnectEvent(LifecycleMetaEventBase):
    sub_type: Literal['connect'] = 'connect'

LifecycleMetaEvent = Annotated[ConnectEvent, Field(discriminator='sub_type')]

class HeartbeatStatus(BaseModel):
    online: bool
    good: bool

class HeartbeatEvent(MetaEventBase):
    meta_event_type: Literal['heartbeat'] = 'heartbeat'
    status: HeartbeatStatus
    interval: int

MetaEvent = Annotated[LifecycleMetaEvent | HeartbeatEvent, Field(discriminator='meta_event_type')]

class TextData(BaseModel):
    text: str

class ReplyData(BaseModel):
    id: int

class ImageData(BaseModel):
    file: str # 如果是接收，则通常是MD5.jpg。如果是发送，"file://D:/a.jpg"、"http://xxx.png"、"base64://xxxxxxxx"
    sub_type: Annotated[Literal[0, 1], '0 is normal image while 1 is a meme']
    url: AnyHttpUrl | None  # 使用 AnyHttpUrl 类型确保 URL 格式有效，如果是发送，可以省略此项
    file_size: int | None # 如果是发送，可以省略此项

    model_config = {"extra": "ignore"}

class VideoData(BaseModel):
    file: str # 如果是接收，则通常是MD5.mp4。如果是发送，"file://D:/a.jpg"、"http://xxx.png"
    url: AnyHttpUrl | None  # 使用 AnyHttpUrl 类型确保 URL 格式有效，如果是发送，可以省略此项
    file_size: int | None # 如果是发送，可以省略此项

    model_config = {"extra": "ignore"}

class FileData(BaseModel):
    file: str
    file_id: str
    url: AnyHttpUrl | None  # 私聊没有群聊有，使用 AnyHttpUrl 类型确保 URL 格式有效

    model_config = {"extra": "ignore"}

class AtData(BaseModel):
    qq: int | Literal["all"]

class ForwardData(BaseModel):
    id: int

class TextMessageSegment(BaseModel):
    type: Literal["text"] = "text"
    data: TextData

class ReplyMessageSegment(BaseModel):
    type: Literal["reply"] = "reply"
    data: ReplyData

class ImageMessageSegment(BaseModel):
    type: Literal["image"] = "image"
    data: ImageData

class VideoMessageSegment(BaseModel):
    type: Literal["video"] = "video"
    data: VideoData

class FileMessageSegment(BaseModel):
    type: Literal["file"] = "file"
    data: FileData

class AtMessageSegment(BaseModel):
    type: Literal["at"] = "at"
    data: AtData

class ForwardMessageSegment(BaseModel):
    type: Literal["forward"] = "forward"
    data: ForwardData

MessageSegment = Annotated[TextMessageSegment | ReplyMessageSegment | ImageMessageSegment | VideoMessageSegment | FileMessageSegment | AtMessageSegment | ForwardMessageSegment, Field(discriminator="type")]
MessageSegmentModel: TypeAdapter[MessageSegment] = TypeAdapter(MessageSegment)

class MessageBase(OneBotEventBase):
    post_type: Literal['message', 'message_sent'] = 'message'
    user_id: int
    message_id: int
    raw_message: str
    message: list[MessageSegment]
    message_format: Literal['array']

class PrivateMessage(MessageBase):
    message_type: Literal["private"] = "private"
    target_id: int

class GroupMessage(MessageBase):
    message_type: Literal["group"] = "group"
    group_id: int

Message = Annotated[PrivateMessage | GroupMessage, Field(discriminator="message_type")]
MessageModel: TypeAdapter[Message] = TypeAdapter(Message)

WsMessage = Annotated[MetaEvent | Message, Field(discriminator="post_type")]
WsMessageModel: TypeAdapter[WsMessage] = TypeAdapter(WsMessage)

setattr(MessageSegmentModel, "model_validate", MessageSegmentModel.validate_python)
setattr(MessageModel, "model_validate", MessageModel.validate_python)
setattr(WsMessageModel, "model_validate", WsMessageModel.validate_python)