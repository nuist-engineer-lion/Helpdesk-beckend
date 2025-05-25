import pytest
from collections.abc import Sequence
from typing import (
    Annotated,
    Any,
    TypeVar
)
from app.core.utils import enhanced_isinstance
from app.schemas.qq import (
    WsMessage,
    PrivateMessage,
    GroupMessage,
    ConnectEvent,
    HeartbeatEvent,
    MessageSegment,
    TextMessageSegment,
    ImageMessageSegment
)

def test_basic_types():
    """测试基本类型检查"""
    assert enhanced_isinstance(42, int)
    assert enhanced_isinstance("hello", str)
    assert enhanced_isinstance(3.14, float)
    assert enhanced_isinstance(True, bool)
    assert enhanced_isinstance(None, type(None))
    assert not enhanced_isinstance(42, str)
    assert not enhanced_isinstance("hello", int)

def test_annotated_types():
    """测试注解类型检查"""
    # 基础注解
    assert enhanced_isinstance(42, Annotated[int, "positive"])
    assert enhanced_isinstance("hello", Annotated[str, "non-empty"])
    
    # 嵌套注解
    assert enhanced_isinstance(42, Annotated[Annotated[int, "positive"], "validated"])
    assert enhanced_isinstance(42, Annotated[Annotated[Annotated[int, "min"], "max"], "range"])
    
    # 带注解的容器
    assert enhanced_isinstance([1, 2, 3], list[Annotated[int, "positive"]])
    assert enhanced_isinstance({"a": 1}, dict[str, Annotated[int, "non-negative"]])

def test_union_types():
    """测试联合类型检查"""
    # Python 3.10+ 语法
    assert enhanced_isinstance(42, int | str)
    assert enhanced_isinstance("hello", int | str)
    assert not enhanced_isinstance(3.14, int | str)
    
    # 嵌套联合类型
    complex_type = list[int | str] | dict[str, float | int]
    assert enhanced_isinstance([1, "hello", 2], complex_type)
    assert enhanced_isinstance({"a": 1, "b": 3.14}, complex_type)
    assert not enhanced_isinstance([1.0, 2.0], complex_type)

def test_container_types():
    """测试容器类型检查"""
    # 列表
    assert enhanced_isinstance([1, 2, 3], list[int])
    assert not enhanced_isinstance([1, "2", 3], list[int])
    
    # 字典
    assert enhanced_isinstance({"a": 1, "b": 2}, dict[str, int])
    assert not enhanced_isinstance({"a": 1, "b": "2"}, dict[str, int])
    
    # 集合
    assert enhanced_isinstance({1, 2, 3}, set[int])
    assert not enhanced_isinstance({1, "2", 3}, set[int])
    
    # 元组
    assert enhanced_isinstance((1, "hello", True), tuple[int, str, bool])
    assert not enhanced_isinstance((1, "hello"), tuple[int, str, bool])
    
    # 不定长元组
    assert enhanced_isinstance((1, 2, 3), tuple[int, ...])
    assert not enhanced_isinstance((1, "2", 3), tuple[int, ...])

def test_nested_container_types():
    """测试嵌套容器类型检查"""
    # 嵌套列表
    assert enhanced_isinstance([[1, 2], [3, 4]], list[list[int]])
    assert not enhanced_isinstance([[1, "2"], [3, 4]], list[list[int]])
    
    # 复杂嵌套
    complex_dict: dict[str, list[int] | list[tuple[int, str]] | set[int | str | float]] = {
        "nums": [1, 2, 3],
        "pairs": [(1, "one"), (2, "two")],
        "mixed": {1, "two", 3.0}
    }
    assert enhanced_isinstance(
        complex_dict,
        dict[str, list[int] | list[tuple[int, str]] | set[int | str | float]]
    )

def test_type_var():
    """测试类型变量"""
    T = TypeVar('T')
    assert enhanced_isinstance(42, T)
    assert enhanced_isinstance("hello", T)
    assert enhanced_isinstance([1, 2, 3], T)

def test_abstract_base_classes():
    """测试抽象基类"""
    # 序列类型
    assert enhanced_isinstance([1, 2, 3], Sequence[int])
    assert enhanced_isinstance((1, 2, 3), Sequence[int])
    assert not enhanced_isinstance({1, 2, 3}, Sequence[int])

def test_edge_cases():
    """测试边缘情况"""
    # Any 类型
    assert enhanced_isinstance(42, Any)
    assert enhanced_isinstance("hello", Any)
    assert enhanced_isinstance(None, Any)
    
    # Optional 类型
    assert enhanced_isinstance(42, int | None)
    assert enhanced_isinstance(None, int | None)
    assert not enhanced_isinstance("42", int | None)
    
    # 空元组
    assert enhanced_isinstance((), tuple[()])
    assert not enhanced_isinstance((1,), tuple[()])
    
    # 复杂嵌套类型
    complex_type = list[dict[str, (int | list[Annotated[str, "metadata"]] | None)]]
    valid_data: list[dict[str, int | list[str] | None]] = [{"key": None}, {"key": 42}, {"key": ["hello", "world"]}]
    assert enhanced_isinstance(valid_data, complex_type)
    
    invalid_data = [{"key": 3.14}]  # float 不是允许的类型
    assert not enhanced_isinstance(invalid_data, complex_type)

def test_custom_types():
    """测试自定义类型"""
    class CustomType:
        pass
    
    class SubType(CustomType):
        pass
    
    obj = SubType()
    assert enhanced_isinstance(obj, CustomType)
    assert enhanced_isinstance(obj, SubType)
    assert not enhanced_isinstance(42, CustomType)

def test_type_nested():
    """测试 type[] 的嵌套情况"""
    # 基本 type[] 测试
    assert enhanced_isinstance(str, type[str])
    assert not enhanced_isinstance(int, type[str])
    assert enhanced_isinstance(int, type[int])
    
    # 容器中的 type[] 测试
    type_list: list[type[Any]] = [str, int]
    assert enhanced_isinstance(type_list, list[type])
    assert enhanced_isinstance(type_list, list[type[Any]])
    
    # 特定类型的列表测试
    str_type_list: list[type[str]] = [str]
    assert enhanced_isinstance(str_type_list, list[type[str]])
    assert not enhanced_isinstance([int], list[type[str]])
    
    # 字典中的 type[] 测试
    type_dict: dict[str, type[Any]] = {"string": str, "integer": int}
    assert enhanced_isinstance(type_dict, dict[str, type])
    assert enhanced_isinstance(type_dict, dict[str, type[Any]])
    
    # 多层嵌套测试
    nested_types: list[type[type]] = [type[str], type[int]]
    assert enhanced_isinstance(nested_types, list[type[type]])
    
    # type 的 type 测试
    assert enhanced_isinstance(type, type[type])
    assert enhanced_isinstance(str, type[Any])

def test_wsmessage_types():
    """测试 WsMessage 相关的类型检查"""
    # 创建测试数据
    current_time = int(1746673640)
    
    # 私聊消息数据
    private_message_data = { # type: ignore
        "self_id": 3892215616,
        "user_id": 5079132,
        "time": current_time,
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
    
    # 群聊消息数据
    group_message_data = { # type: ignore
        "self_id": 3892215616,
        "user_id": 5079132,
        "time": current_time,
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
    
    # 连接事件数据
    connect_event_data = { # type: ignore
        "time": current_time,
        "self_id": 3892215616,
        "post_type": "meta_event",
        "meta_event_type": "lifecycle",
        "sub_type": "connect"
    }
    
    # 心跳事件数据
    heartbeat_event_data = { # type: ignore
        "time": current_time,
        "self_id": 3892215616,
        "post_type": "meta_event",
        "meta_event_type": "heartbeat",
        "status": {
            "online": True,
            "good": True
        },
        "interval": 30000
    }
    
    # 创建对象实例
    private_message = PrivateMessage.model_validate(private_message_data)
    group_message = GroupMessage.model_validate(group_message_data)
    connect_event = ConnectEvent.model_validate(connect_event_data)
    heartbeat_event = HeartbeatEvent.model_validate(heartbeat_event_data)
    
    # 测试具体类型与WsMessage的关系
    assert enhanced_isinstance(private_message, WsMessage)
    assert enhanced_isinstance(group_message, WsMessage)
    assert enhanced_isinstance(connect_event, WsMessage)
    assert enhanced_isinstance(heartbeat_event, WsMessage)
    
    # 测试具体类型
    assert enhanced_isinstance(private_message, PrivateMessage)
    assert enhanced_isinstance(group_message, GroupMessage)
    assert enhanced_isinstance(connect_event, ConnectEvent)
    assert enhanced_isinstance(heartbeat_event, HeartbeatEvent)
    
    # 测试类型检查的准确性
    assert not enhanced_isinstance(private_message, GroupMessage)
    assert not enhanced_isinstance(group_message, PrivateMessage)
    assert not enhanced_isinstance(connect_event, HeartbeatEvent)
    assert not enhanced_isinstance(heartbeat_event, ConnectEvent)
    
    # 测试MessageSegment相关
    text_segment_data = { # type: ignore
        "type": "text",
        "data": {
            "text": "你好"
        }
    }
    
    image_segment_data = { # type: ignore
        "type": "image",
        "data": {
            "file": "test.png",
            "sub_type": 0,
            "url": "https://example.com/test.png"
        }
    }
    
    text_segment = TextMessageSegment.model_validate(text_segment_data)
    image_segment = ImageMessageSegment.model_validate(image_segment_data)
    
    # 测试MessageSegment类型检查
    assert enhanced_isinstance(text_segment, MessageSegment)
    assert enhanced_isinstance(image_segment, MessageSegment)
    assert enhanced_isinstance(text_segment, TextMessageSegment)
    assert enhanced_isinstance(image_segment, ImageMessageSegment)
    assert not enhanced_isinstance(text_segment, ImageMessageSegment)
    assert not enhanced_isinstance(image_segment, TextMessageSegment)
    
    # 测试容器中的WsMessage类型
    ws_messages = [private_message, group_message, connect_event, heartbeat_event] # type: ignore
    assert enhanced_isinstance(ws_messages, list[WsMessage])
    
    # 测试混合类型列表
    message_segments = [text_segment, image_segment] # type: ignore
    assert enhanced_isinstance(message_segments, list[MessageSegment])
    
    # 测试复杂嵌套类型
    complex_data = { # type: ignore
        "messages": ws_messages,
        "segments": message_segments
    }
    assert enhanced_isinstance(complex_data, dict[str, list[WsMessage] | list[MessageSegment]])
    
    # 测试 PrivateMessage 类型检查
    assert enhanced_isinstance(PrivateMessage, type[PrivateMessage])
    assert enhanced_isinstance(GroupMessage, type[GroupMessage])
    assert enhanced_isinstance(ConnectEvent, type[ConnectEvent])
    assert enhanced_isinstance(HeartbeatEvent, type[HeartbeatEvent])
    
    # 测试不同类型之间的检查
    assert not enhanced_isinstance(GroupMessage, type[PrivateMessage])  # GroupMessage 不是 PrivateMessage 类型
    assert not enhanced_isinstance(PrivateMessage, type[GroupMessage])  # PrivateMessage 不是 GroupMessage 类型
    assert not enhanced_isinstance(ConnectEvent, type[HeartbeatEvent])  # ConnectEvent 不是 HeartbeatEvent 类型
    
    # 测试非相关类型
    assert not enhanced_isinstance(str, type[PrivateMessage])
    assert not enhanced_isinstance(int, type[GroupMessage])
    assert not enhanced_isinstance(TextMessageSegment, type[ConnectEvent])
    
    # 测试容器中的具体类型
    private_message_types = [PrivateMessage] # type: ignore
    assert enhanced_isinstance(private_message_types, list[type[PrivateMessage]])
    
    group_message_types = [GroupMessage] # type: ignore
    assert enhanced_isinstance(group_message_types, list[type[GroupMessage]])
    
    # 测试混合具体类型列表
    message_types = [PrivateMessage, GroupMessage] # type: ignore
    assert not enhanced_isinstance(message_types, list[type[PrivateMessage]])  # 包含非 PrivateMessage 类型
    assert not enhanced_isinstance(message_types, list[type[GroupMessage]])    # 包含非 GroupMessage 类型
    
    # 测试字典中的具体类型
    specific_type_mapping = { # type: ignore
        "private": PrivateMessage,
        "group": GroupMessage
    }
    # 这个测试应该通过，因为都是具体的消息类型
    assert enhanced_isinstance({"private": PrivateMessage}, dict[str, type[PrivateMessage]])
    assert enhanced_isinstance({"group": GroupMessage}, dict[str, type[GroupMessage]])
    
    # 重新添加对复杂联合类型的测试
    # 测试 type[WsMessage] 类型检查 - 现在应该能够处理复杂的联合类型
    assert enhanced_isinstance(PrivateMessage, type[WsMessage])
    assert enhanced_isinstance(GroupMessage, type[WsMessage])
    assert enhanced_isinstance(ConnectEvent, type[WsMessage])
    assert enhanced_isinstance(HeartbeatEvent, type[WsMessage])
    
    # 测试非 WsMessage 类型
    assert not enhanced_isinstance(str, type[WsMessage])
    assert not enhanced_isinstance(int, type[WsMessage])
    assert not enhanced_isinstance(TextMessageSegment, type[WsMessage])
    
    # 测试容器中的 type[WsMessage]
    wsmessage_types = [PrivateMessage, GroupMessage, ConnectEvent, HeartbeatEvent] # type: ignore
    assert enhanced_isinstance(wsmessage_types, list[type[WsMessage]])
    
    # 测试混合类型列表（包含非 WsMessage 类型）
    mixed_types = [PrivateMessage, GroupMessage, str, int] # type: ignore
    assert not enhanced_isinstance(mixed_types, list[type[WsMessage]])
    
    # 测试字典中的 type[WsMessage]
    type_mapping = { # type: ignore
        "private": PrivateMessage,
        "group": GroupMessage,
        "connect": ConnectEvent,
        "heartbeat": HeartbeatEvent
    }
    assert enhanced_isinstance(type_mapping, dict[str, type[WsMessage]])


if __name__ == '__main__':
    pytest.main([__file__])
