#!/usr/bin/env python3
"""
简单的WebSocket客户端示例
"""

import asyncio
import json
import time
import websockets
from loguru import logger

async def simple_client():
    """简单的客户端连接示例"""
    uri = "ws://127.0.0.1:8000/ws/"
    bot_id = 12345
    
    try:
        # 连接到WebSocket服务器
        logger.info(f"正在连接到 {uri}...")
        websocket = await websockets.connect(uri)
        logger.info("连接成功!")
        
        # 发送连接事件进行握手
        connect_event = {
            "time": int(time.time()),
            "self_id": bot_id,
            "post_type": "meta_event",
            "meta_event_type": "lifecycle",
            "sub_type": "connect"
        }
        
        await websocket.send(json.dumps(connect_event))
        logger.info("已发送握手消息")
        
        # 发送一条测试消息
        test_message = {
            "time": int(time.time()),
            "self_id": bot_id,
            "post_type": "message",
            "message_type": "private",
            "user_id": bot_id,
            "message_id": int(time.time() * 1000),
            "target_id": 67890,  # 目标用户ID
            "raw_message": "Hello from WebSocket client!",
            "message": [{
                "type": "text",
                "data": {"text": "Hello from WebSocket client!"}
            }],
            "message_format": "array"
        }
        
        await websocket.send(json.dumps(test_message, ensure_ascii=False))
        logger.info("已发送测试消息")
        
        # 监听服务器响应（等待5秒）
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            logger.info(f"收到服务器响应: {response}")
        except asyncio.TimeoutError:
            logger.info("5秒内未收到服务器响应")
        
        # 发送心跳消息
        heartbeat = {
            "time": int(time.time()),
            "self_id": bot_id,
            "post_type": "meta_event",
            "meta_event_type": "heartbeat",
            "status": {
                "online": True,
                "good": True
            },
            "interval": 30000
        }
        
        await websocket.send(json.dumps(heartbeat))
        logger.info("已发送心跳消息")
        
        # 关闭连接
        await websocket.close()
        logger.info("连接已关闭")
        
    except Exception as e:
        logger.error(f"连接失败: {e}")

if __name__ == "__main__":
    # 配置日志
    logger.remove()  # 移除默认处理器
    logger.add(lambda msg: print(msg, end=""), level="INFO")
    
    # 运行客户端
    asyncio.run(simple_client())
