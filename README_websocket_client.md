# WebSocket客户端

本项目提供了两个WebSocket客户端，用于连接到 `http://127.0.0.1:8000/ws/` 端点。

## 文件说明

### 1. ws_client.py
功能完整的WebSocket客户端类，提供以下特性：
- 自动重连机制
- 事件回调系统
- 消息发送和接收
- 心跳保持
- 错误处理

### 2. simple_client.py
简单的示例客户端，演示基本的连接和消息发送。

## 安装依赖

```bash
pip install websockets loguru
```

## 使用方法

### 简单使用示例

```python
# 运行简单客户端
python simple_client.py
```

### 使用完整客户端类

```python
import asyncio
from ws_client import WebSocketClient

async def message_handler(data):
    print(f"收到消息: {data}")

async def connect_handler():
    print("连接成功!")

async def main():
    # 创建客户端
    client = WebSocketClient(
        uri="ws://127.0.0.1:8000/ws/",
        bot_id=12345,
        reconnect_interval=5,
        max_reconnect_attempts=0  # 0表示无限重连
    )
    
    # 设置回调
    client.on_message(message_handler)
    client.on_connect(connect_handler)
    
    # 启动客户端
    await client.run()

if __name__ == "__main__":
    asyncio.run(main())
```

## 客户端特性

### WebSocket协议要求

根据服务端实现，客户端需要：

1. **连接握手**: 连接后立即发送ConnectEvent消息
2. **消息格式**: 遵循OneBot v11协议格式
3. **心跳保持**: 定期发送心跳消息

### 消息类型

#### 连接事件 (ConnectEvent)
```json
{
    "time": 1640995200,
    "self_id": 12345,
    "post_type": "meta_event",
    "meta_event_type": "lifecycle",
    "sub_type": "connect"
}
```

#### 心跳事件 (HeartbeatEvent)
```json
{
    "time": 1640995200,
    "self_id": 12345,
    "post_type": "meta_event",
    "meta_event_type": "heartbeat",
    "status": {
        "online": true,
        "good": true
    },
    "interval": 30000
}
```

#### 文本消息 (私聊)
```json
{
    "time": 1640995200,
    "self_id": 12345,
    "post_type": "message",
    "message_type": "private",
    "user_id": 12345,
    "message_id": 1640995200000,
    "target_id": 67890,
    "raw_message": "Hello, World!",
    "message": [
        {
            "type": "text",
            "data": {"text": "Hello, World!"}
        }
    ],
    "message_format": "array"
}
```

#### 文本消息 (群聊)
```json
{
    "time": 1640995200,
    "self_id": 12345,
    "post_type": "message",
    "message_type": "group",
    "user_id": 12345,
    "message_id": 1640995200000,
    "group_id": 123456,
    "raw_message": "Hello, Group!",
    "message": [
        {
            "type": "text",
            "data": {"text": "Hello, Group!"}
        }
    ],
    "message_format": "array"
}
```

## WebSocketClient API

### 构造函数参数
- `uri`: WebSocket服务器地址（默认: "ws://127.0.0.1:8000/ws/"）
- `bot_id`: 机器人ID（默认: 12345）
- `reconnect_interval`: 重连间隔秒数（默认: 5）
- `max_reconnect_attempts`: 最大重连次数（默认: 0，表示无限重连）

### 主要方法
- `connect()`: 连接到服务器
- `disconnect()`: 断开连接
- `run()`: 启动客户端主循环
- `send_message(message)`: 发送自定义消息
- `send_text(text, message_type, target_id, group_id)`: 发送文本消息
- `create_connect_event()`: 创建连接事件
- `create_heartbeat_event()`: 创建心跳事件
- `create_text_message()`: 创建文本消息

### 回调方法
- `on_message(callback)`: 设置消息接收回调
- `on_connect(callback)`: 设置连接建立回调
- `on_disconnect(callback)`: 设置连接断开回调
- `on_error(callback)`: 设置错误处理回调

## 注意事项

1. **服务器要求**: 确保服务器运行在 `127.0.0.1:8000`
2. **握手超时**: 服务器要求连接后1秒内发送ConnectEvent，否则会断开连接
3. **消息格式**: 所有消息必须是有效的JSON格式
4. **Bot ID**: 每个客户端应使用唯一的bot_id
5. **重连机制**: 客户端支持自动重连，可配置重连次数和间隔

## 错误处理

客户端包含完善的错误处理机制：
- 连接失败自动重试
- JSON解析错误处理
- WebSocket连接异常处理
- 网络中断自动重连

## 日志输出

客户端使用loguru库进行日志记录，支持：
- 控制台输出
- 文件日志记录
- 日志轮转
- 不同日志级别

## 示例场景

### 发送私聊消息
```python
await client.send_text("Hello!", "private", target_id=67890)
```

### 发送群聊消息
```python
await client.send_text("Hello, everyone!", "group", group_id=123456)
```

### 发送心跳
```python
heartbeat = client.create_heartbeat_event()
await client.send_message(heartbeat)
```

## 故障排除

1. **连接失败**: 检查服务器是否运行在正确端口
2. **握手超时**: 确保ConnectEvent消息格式正确
3. **消息发送失败**: 检查消息格式是否符合OneBot v11规范
4. **重连失败**: 检查网络连接和服务器状态
