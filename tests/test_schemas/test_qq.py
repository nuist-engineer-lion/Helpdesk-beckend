import pytest
from datetime import datetime
from typing import Any
from pydantic import ValidationError
from app.schemas.qq import (
    OneBotEventBase,
    ConnectEvent,
    HeartbeatEvent,
    PrivateMessage,
    GroupMessage,
    TextMessageSegment,
    ReplyMessageSegment,
    ImageMessageSegment,
    VideoMessageSegment,
    FileMessageSegment,
    AtMessageSegment,
    ForwardMessageSegment,
    WsMessageModel
)


class TestOneBotEventBase:
    def test_validate_timestamp(self):
        # 测试正常时间戳
        current_time = int(datetime.now().timestamp())
        event = OneBotEventBase(time=current_time, self_id=123456789)
        assert event.time == current_time

        # 测试时间戳为0
        with pytest.raises(ValidationError) as excinfo:
            OneBotEventBase(time=0, self_id=123456789)
        assert "时间戳必须大于0" in str(excinfo.value)

        # 测试时间戳超过当前时间太多
        future_time = current_time + 100000
        with pytest.raises(ValidationError) as excinfo:
            OneBotEventBase(time=future_time, self_id=123456789)
        assert "时间戳不能超过当前时间太多" in str(excinfo.value)


class TestMetaEvent:
    def test_connect_event(self):
        # 测试连接事件
        json_data: dict[str,Any] = {
            "time": 1746673610,
            "self_id": 3892215616,
            "post_type": "meta_event",
            "meta_event_type": "lifecycle",
            "sub_type": "connect"
        }
        event = ConnectEvent.model_validate(json_data)
        assert isinstance(event, ConnectEvent)
        assert event.time == 1746673610
        assert event.self_id == 3892215616
        assert event.post_type == "meta_event"
        assert event.meta_event_type == "lifecycle"
        assert event.sub_type == "connect"

    def test_heartbeat_event(self):
        # 测试心跳事件
        json_data: dict[str,Any] = {
            "time": 1746673666,
            "self_id": 3892215616,
            "post_type": "meta_event",
            "meta_event_type": "heartbeat",
            "status": {
                "online": True,
                "good": True
            },
            "interval": 30000
        }
        event = HeartbeatEvent.model_validate(json_data)
        assert isinstance(event, HeartbeatEvent)
        assert event.time == 1746673666
        assert event.self_id == 3892215616
        assert event.post_type == "meta_event"
        assert event.meta_event_type == "heartbeat"
        assert event.status.online is True
        assert event.status.good is True
        assert event.interval == 30000


class TestMessageSegment:
    def test_text_segment(self):
        json_data: dict[str,Any] = {
            "type": "text",
            "data": {
                "text": "你好"
            }
        }
        segment = TextMessageSegment.model_validate(json_data)
        assert isinstance(segment, TextMessageSegment)
        assert segment.type == "text"
        assert segment.data.text == "你好"

    def test_reply_segment(self):
        json_data: dict[str,Any] = {
            "type": "reply",
            "data": {
                "id": "1136053690"
            }
        }
        segment = ReplyMessageSegment.model_validate(json_data)
        assert isinstance(segment, ReplyMessageSegment)
        assert segment.type == "reply"
        assert segment.data.id == 1136053690  # 验证字符串ID被转换为整数

    def test_image_segment(self):
        json_data: dict[str,Any] = {
            "type": "image",
            "data": {
                "file": "2490A74D2F133CC4D491994263FA51A9.png",
                "sub_type": 0,
                "url": "https://multimedia.nt.qq.com.cn/download?appid=1406&fileid=EhQ7zBU4i9BPJTs7Is8Z1hI03P0MhhigNyD-Cii5qJb99pKNAzIEcHJvZFoQCtlD7JGNXCz-J7GQthR1SHoCwOw&rkey=CAQSMIWZoZblav5noN2bkE4qDbEk2GVQii_LWu9AtTRtZMKbTmJEER87ZQjBY0V0SRJ5eA"
            }
        }
        segment = ImageMessageSegment.model_validate(json_data)
        assert isinstance(segment, ImageMessageSegment)
        assert segment.type == "image"
        assert segment.data.file == "2490A74D2F133CC4D491994263FA51A9.png"
        assert segment.data.sub_type == 0
        assert str(segment.data.url).startswith("https://multimedia.nt.qq.com.cn/download")

    def test_video_segment(self):
        json_data: dict[str,Any] = {
            "type": "video",
            "data": {
                "file": "e8996238c43fed13f729cc50fa63247e.mp4",
                "url": "https://multimedia.nt.qq.com.cn/download?appid=1413&format=origin&orgfmt=t264&spec=0&rkey=CAMSmAGl6TZaIgA9RLAyCen1vjFZ5kpF1d3PMHFagjRyu1w3ho5oETvf0k0jkA6467zu9ba5kW_-lK0hWBEVOtUGIqXPVE7DyohqMqCCoORV4ZrAhfoXBJQ7a73cZ-ZEw9kGVsXTumaiPtErgDO6ZVbBB5xQAs6ZyBVHgmTo2ZEVQc-ULH9Yk8Od7kCAqqyThGz4w364TlpSA8CA4Q"
            }
        }
        segment = VideoMessageSegment.model_validate(json_data)
        assert isinstance(segment, VideoMessageSegment)
        assert segment.type == "video"
        assert segment.data.file == "e8996238c43fed13f729cc50fa63247e.mp4"
        assert str(segment.data.url).startswith("https://multimedia.nt.qq.com.cn/download")

    def test_file_segment(self):
        json_data: dict[str,Any] = {
            "type": "file",
            "data": {
                "file": "到底是谁发明的外包？！ [BV147G1zQEri_p1].mp4",
                "file_id": "5c804d00f95b09df4de35ea1c783c368_f798da46-2c17-11f0-bf38-8307ae91f46d",
                "url": "https://tjc-download.ftn.qq.com/ftn_handler/f0f728248fe401d3ead06a53a885d62b5baa1d8a148f5ba9beaeba1e76c259fc4b7e13b6318a9aaae4a835cab852eea66f66ac7ce30a11eb6ddc1a63dce3547c/?fname="
            }
        }
        segment = FileMessageSegment.model_validate(json_data)
        assert isinstance(segment, FileMessageSegment)
        assert segment.type == "file"
        assert segment.data.file == "到底是谁发明的外包？！ [BV147G1zQEri_p1].mp4"
        assert segment.data.file_id == "5c804d00f95b09df4de35ea1c783c368_f798da46-2c17-11f0-bf38-8307ae91f46d"
        assert str(segment.data.url).startswith("https://tjc-download.ftn.qq.com/ftn_handler/")  # 验证URL格式

    def test_at_segment(self):
        json_data: dict[str,Any] = {
            "type": "at",
            "data": {
                "qq": "all"
            }
        }
        segment = AtMessageSegment.model_validate(json_data)
        assert isinstance(segment, AtMessageSegment)
        assert segment.type == "at"
        assert segment.data.qq == "all"

        json_data = {
            "type": "at",
            "data": {
                "qq": "1090558688"
            }
        }
        segment = AtMessageSegment.model_validate(json_data)
        assert isinstance(segment, AtMessageSegment)
        assert segment.type == "at"
        assert segment.data.qq == 1090558688  # 验证字符串ID被转换为整数

    def test_forward_segment(self):
        json_data: dict[str,Any] = {
            "type": "forward",
            "data": {
                "id": "7505442611578883339"
            }
        }
        segment = ForwardMessageSegment.model_validate(json_data)
        assert isinstance(segment, ForwardMessageSegment)
        assert segment.type == "forward"
        assert segment.data.id == 7505442611578883339  # 验证字符串ID被转换为整数


class TestMessage:
    def test_private_message(self):
        json_data: dict[str,Any] = {
            "self_id": 3892215616,
            "user_id": 5079132,
            "time": 1746673640,
            "message_id": 1136053690,
            "message_seq": 1136053690,
            "real_id": 1136053690,
            "real_seq": "770",
            "message_type": "private",
            "sender": {
                "user_id": 5079132,
                "nickname": "东风寄千愁",
                "card": ""
            },
            "raw_message": "你好",
            "font": 14,
            "sub_type": "friend",
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": "你好"
                    }
                }
            ],
            "message_format": "array",
            "post_type": "message",
            "target_id": 5079132
        }
        message = PrivateMessage.model_validate(json_data)
        assert isinstance(message, PrivateMessage)
        assert message.self_id == 3892215616
        assert message.user_id == 5079132
        assert message.time == 1746673640
        assert message.message_id == 1136053690
        assert message.raw_message == "你好"
        assert message.message_type == "private"
        assert message.target_id == 5079132
        assert len(message.message) == 1
        assert isinstance(message.message[0], TextMessageSegment)
        assert message.message[0].data.text == "你好"

    def test_private_message_with_reply_and_image(self):
        json_data: dict[str,Any] = {
            "self_id": 3892215616,
            "user_id": 5079132,
            "time": 1746674878,
            "message_id": 1352199344,
            "message_seq": 1352199344,
            "real_id": 1352199344,
            "real_seq": "773",
            "message_type": "private",
            "sender": {
                "user_id": 5079132,
                "nickname": "东风寄千愁",
                "card": ""
            },
            "raw_message": "哈哈[CQ:image,file=2490A74D2F133CC4D491994263FA51A9.png,sub_type=0,url=https://multimedia.nt.qq.com.cn/download?appid=1406&fileid=EhQ7zBU4i9BPJTs7Is8Z1hI03P0MhhigNyD-Cii5qJb99pKNAzIEcHJvZFoQCtlD7JGNXCz-J7GQthR1SHoCwOw&rkey=CAQSMIWZoZblav5noN2bkE4qDbEk2GVQii_LWu9AtTRtZMKbTmJEER87ZQjBY0V0SRJ5eA,file_size=7072]啊啊",
            "font": 14,
            "sub_type": "friend",
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": "哈哈"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "summary": "",
                        "file": "2490A74D2F133CC4D491994263FA51A9.png",
                        "sub_type": 0,
                        "url": "https://multimedia.nt.qq.com.cn/download?appid=1406&fileid=EhQ7zBU4i9BPJTs7Is8Z1hI03P0MhhigNyD-Cii5qJb99pKNAzIEcHJvZFoQCtlD7JGNXCz-J7GQthR1SHoCwOw&rkey=CAQSMIWZoZblav5noN2bkE4qDbEk2GVQii_LWu9AtTRtZMKbTmJEER87ZQjBY0V0SRJ5eA",
                        "file_size": "7072"
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": "啊啊"
                    }
                }
            ],
            "message_format": "array",
            "post_type": "message",
            "target_id": 5079132
        }
        message = PrivateMessage.model_validate(json_data)
        assert isinstance(message, PrivateMessage)
        assert message.self_id == 3892215616
        assert message.user_id == 5079132
        assert message.time == 1746674878
        assert message.message_id == 1352199344
        assert message.message_type == "private"
        assert message.target_id == 5079132
        assert len(message.message) == 3
        assert isinstance(message.message[0], TextMessageSegment)
        assert message.message[0].data.text == "哈哈"
        assert isinstance(message.message[1], ImageMessageSegment)
        assert message.message[1].data.file == "2490A74D2F133CC4D491994263FA51A9.png"
        assert message.message[1].data.sub_type == 0
        assert isinstance(message.message[2], TextMessageSegment)
        assert message.message[2].data.text == "啊啊"

    def test_group_message(self):
        json_data: dict[str,Any] = {
            "self_id": 3892215616,
            "user_id": 5079132,
            "time": 1747107314,
            "message_id": 2096329721,
            "message_seq": 2096329721,
            "real_id": 2096329721,
            "real_seq": "20471",
            "message_type": "group",
            "sender": {
                "user_id": 5079132,
                "nickname": "东风寄千愁",
                "card": "",
                "role": "admin"
            },
            "raw_message": "test",
            "font": 14,
            "sub_type": "normal",
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": "test"
                    }
                }
            ],
            "message_format": "array",
            "post_type": "message",
            "group_id": 757951413
        }
        message = GroupMessage.model_validate(json_data)
        assert isinstance(message, GroupMessage)
        assert message.self_id == 3892215616
        assert message.user_id == 5079132
        assert message.time == 1747107314
        assert message.message_id == 2096329721
        assert message.raw_message == "test"
        assert message.message_type == "group"
        assert message.group_id == 757951413
        assert len(message.message) == 1
        assert isinstance(message.message[0], TextMessageSegment)
        assert message.message[0].data.text == "test"

    def test_complex_group_message(self):
        json_data: dict[str,Any] = {
            "self_id": 3892215616,
            "user_id": 5079132,
            "time": 1747107572,
            "message_id": 361878627,
            "message_seq": 361878627,
            "real_id": 361878627,
            "real_seq": "20472",
            "message_type": "group",
            "sender": {
                "user_id": 5079132,
                "nickname": "东风寄千愁",
                "card": "",
                "role": "admin"
            },
            "raw_message": "[CQ:reply,id=265662236][CQ:at,qq=all] test message[CQ:at,qq=1090558688][CQ:image,file=E8C195761CEDA1D66763414CB8EE494E.png,sub_type=0,url=https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=EhTeJv9whzV7da8HpZ1A_wPjgvK_ohjTSCD_CijvnL3xwp-NAzIEcHJvZFCAvaMBWhAepoWqDDM35uuv21_CACsGegLJ7g&rkey=CAISMIPGBhlMPqo7xpuFl7uQs7MbOgWDdV0-0g5bo1WQdV54LtbgFiqjY4SrkyuvDe4i3g,file_size=9299]",
            "font": 14,
            "sub_type": "normal",
            "message": [
                {
                    "type": "reply",
                    "data": {
                        "id": "265662236"
                    }
                },
                {
                    "type": "at",
                    "data": {
                        "qq": "all"
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": " test message"
                    }
                },
                {
                    "type": "at",
                    "data": {
                        "qq": "1090558688"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "summary": "",
                        "file": "E8C195761CEDA1D66763414CB8EE494E.png",
                        "sub_type": 0,
                        "url": "https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=EhTeJv9whzV7da8HpZ1A_wPjgvK_ohjTSCD_CijvnL3xwp-NAzIEcHJvZFCAvaMBWhAepoWqDDM35uuv21_CACsGegLJ7g&rkey=CAISMIPGBhlMPqo7xpuFl7uQs7MbOgWDdV0-0g5bo1WQdV54LtbgFiqjY4SrkyuvDe4i3g",
                        "file_size": "9299"
                    }
                }
            ],
            "message_format": "array",
            "post_type": "message",
            "group_id": 757951413
        }
        message = GroupMessage.model_validate(json_data)
        assert isinstance(message, GroupMessage)
        assert message.self_id == 3892215616
        assert message.user_id == 5079132
        assert message.time == 1747107572
        assert message.message_id == 361878627
        assert message.message_type == "group"
        assert message.group_id == 757951413
        assert len(message.message) == 5
        assert isinstance(message.message[0], ReplyMessageSegment)
        assert message.message[0].data.id == 265662236
        assert isinstance(message.message[1], AtMessageSegment)
        assert message.message[1].data.qq == "all"
        assert isinstance(message.message[2], TextMessageSegment)
        assert message.message[2].data.text == " test message"
        assert isinstance(message.message[3], AtMessageSegment)
        assert message.message[3].data.qq == 1090558688
        assert isinstance(message.message[4], ImageMessageSegment)
        assert message.message[4].data.file == "E8C195761CEDA1D66763414CB8EE494E.png"


class TestWsMessage:
    def test_ws_message_meta_event(self):
        # 测试元事件
        json_data: dict[str,Any] = {
            "time": 1746673610,
            "self_id": 3892215616,
            "post_type": "meta_event",
            "meta_event_type": "lifecycle",
            "sub_type": "connect"
        }
        message = ConnectEvent.model_validate(json_data)
        assert isinstance(message, ConnectEvent)
        assert message.post_type == "meta_event"
        assert message.meta_event_type == "lifecycle"
        assert message.sub_type == "connect"

    def test_ws_message_private_message(self):
        # 测试私聊消息
        json_data: dict[str,Any] = {
            "self_id": 3892215616,
            "user_id": 5079132,
            "time": 1746673640,
            "message_id": 1136053690,
            "message_seq": 1136053690,
            "real_id": 1136053690,
            "real_seq": "770",
            "message_type": "private",
            "sender": {
                "user_id": 5079132,
                "nickname": "东风寄千愁",
                "card": ""
            },
            "raw_message": "你好",
            "font": 14,
            "sub_type": "friend",
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": "你好"
                    }
                }
            ],
            "message_format": "array",
            "post_type": "message",
            "target_id": 5079132
        }
        message = PrivateMessage.model_validate(json_data)
        assert isinstance(message, PrivateMessage)
        assert message.post_type == "message"
        assert message.message_type == "private"
        assert message.raw_message == "你好"

    def test_ws_message_group_message(self):
        # 测试群聊消息
        json_data: dict[str,Any] = {
            "self_id": 3892215616,
            "user_id": 5079132,
            "time": 1747107314,
            "message_id": 2096329721,
            "message_seq": 2096329721,
            "real_id": 2096329721,
            "real_seq": "20471",
            "message_type": "group",
            "sender": {
                "user_id": 5079132,
                "nickname": "东风寄千愁",
                "card": "",
                "role": "admin"
            },
            "raw_message": "test",
            "font": 14,
            "sub_type": "normal",
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": "test"
                    }
                }
            ],
            "message_format": "array",
            "post_type": "message",
            "group_id": 757951413
        }
        message = GroupMessage.model_validate(json_data)
        assert isinstance(message, GroupMessage)
        assert message.post_type == "message"
        assert message.message_type == "group"
        assert message.raw_message == "test"
        assert message.group_id == 757951413

    def test_ws_message_discriminator(self):
        # 测试使用 WsMessage作为基类的 discriminator
        
        # 测试连接事件
        json_data: dict[str,Any] = {
            "time": 1746673610,
            "self_id": 3892215616,
            "post_type": "meta_event",
            "meta_event_type": "lifecycle",
            "sub_type": "connect"
        }
        message = WsMessageModel.validate_python(json_data)
        assert isinstance(message, ConnectEvent)
        
        # 测试心跳事件
        json_data = {
            "time": 1746673666,
            "self_id": 3892215616,
            "post_type": "meta_event",
            "meta_event_type": "heartbeat",
            "status": {
                "online": True,
                "good": True
            },
            "interval": 30000
        }
        message = WsMessageModel.validate_python(json_data)
        assert isinstance(message, HeartbeatEvent)
        
        # 测试私聊消息
        json_data = {
            "self_id": 3892215616,
            "user_id": 5079132,
            "time": 1746673640,
            "message_id": 1136053690,
            "message_seq": 1136053690,
            "real_id": 1136053690,
            "real_seq": "770",
            "message_type": "private",
            "sender": {
                "user_id": 5079132,
                "nickname": "东风寄千愁",
                "card": ""
            },
            "raw_message": "你好",
            "font": 14,
            "sub_type": "friend",
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": "你好"
                    }
                }
            ],
            "message_format": "array",
            "post_type": "message",
            "target_id": 5079132
        }
        message = WsMessageModel.validate_python(json_data)
        assert isinstance(message, PrivateMessage)
        
        # 测试群聊消息
        json_data = {
            "self_id": 3892215616,
            "user_id": 5079132,
            "time": 1747107314,
            "message_id": 2096329721,
            "message_seq": 2096329721,
            "real_id": 2096329721,
            "real_seq": "20471",
            "message_type": "group",
            "sender": {
                "user_id": 5079132,
                "nickname": "东风寄千愁",
                "card": "",
                "role": "admin"
            },
            "raw_message": "test",
            "font": 14,
            "sub_type": "normal",
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": "test"
                    }
                }
            ],
            "message_format": "array",
            "post_type": "message",
            "group_id": 757951413
        }
        message = WsMessageModel.validate_python(json_data)
        assert isinstance(message, GroupMessage)
