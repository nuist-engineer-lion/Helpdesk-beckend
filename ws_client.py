#!/usr/bin/env python3
"""
WebSocket客户端，用于连接到http://127.0.0.1:8000/ws/端点
"""

import asyncio
import json
import time
from typing import Any, Dict, Optional
from collections.abc import Callable
import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedError
from loguru import logger

class WebSocketClient:
    """WebSocket客户端类"""
    
    def __init__(self, 
                 uri: str = "ws://127.0.0.1:8000/ws/",
                 bot_id: int = 12345,
                 reconnect_interval: int = 5,
                 max_reconnect_attempts: int = 0):  # 0表示无限重连
        """
        初始化WebSocket客户端
        
        Args:
            uri: WebSocket服务器地址
            bot_id: 机器人ID
            reconnect_interval: 重连间隔（秒）
            max_reconnect_attempts: 最大重连次数（0为无限重连）
        """
        self.uri = uri
        self.bot_id = bot_id
        self.reconnect_interval = reconnect_interval
        self.max_reconnect_attempts = max_reconnect_attempts
        self.websocket: Optional[Any] = None
        self.is_running = False
        self.reconnect_count = 0
        
        # 事件回调函数
        self.on_message_callback: Optional[Callable] = None
        self.on_connect_callback: Optional[Callable] = None
        self.on_disconnect_callback: Optional[Callable] = None
        self.on_error_callback: Optional[Callable] = None

    def create_connect_event(self) -> Dict[str, Any]:
        """创建连接事件消息"""
        return {
            "time": int(time.time()),
            "self_id": self.bot_id,
            "post_type": "meta_event",
            "meta_event_type": "lifecycle",
            "sub_type": "connect"
        }

    def create_heartbeat_event(self) -> Dict[str, Any]:
        """创建心跳事件消息"""
        return {
            "time": int(time.time()),
            "self_id": self.bot_id,
            "post_type": "meta_event",
            "meta_event_type": "heartbeat",
            "status": {
                "online": True,
                "good": True
            },
            "interval": 30000  # 30秒间隔
        }

    def create_text_message(self, text: str, message_type: str = "private", 
                           target_id: Optional[int] = None, group_id: Optional[int] = None) -> Dict[str, Any]:
        """创建文本消息"""
        message = {
            "time": int(time.time()),
            "self_id": self.bot_id,
            "post_type": "message",
            "message_type": message_type,
            "user_id": self.bot_id,
            "message_id": int(time.time() * 1000),  # 使用时间戳作为消息ID
            "raw_message": text,
            "message": [{
                "type": "text",
                "data": {"text": text}
            }],
            "message_format": "array"
        }
        
        if message_type == "private" and target_id:
            message["target_id"] = target_id
        elif message_type == "group" and group_id:
            message["group_id"] = group_id
            
        return message

    async def send_message(self, message: Dict[str, Any]) -> bool:
        """发送消息到服务器"""
        if not self.websocket:
            logger.error("WebSocket连接未建立")
            return False
            
        try:
            await self.websocket.send(json.dumps(message, ensure_ascii=False))
            logger.info(f"消息发送成功: {message.get('post_type', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False

    async def send_text(self, text: str, message_type: str = "private", 
                       target_id: Optional[int] = None, group_id: Optional[int] = None) -> bool:
        """发送文本消息的便捷方法"""
        message = self.create_text_message(text, message_type, target_id, group_id)
        return await self.send_message(message)

    async def handle_message(self, message: str):
        """处理接收到的消息"""
        try:
            data = json.loads(message)
            logger.info(f"收到消息: {data}")
            
            if self.on_message_callback:
                if asyncio.iscoroutinefunction(self.on_message_callback):
                    await self.on_message_callback(data)
                else:
                    self.on_message_callback(data)
                
        except json.JSONDecodeError:
            logger.error(f"接收到无效的JSON消息: {message}")
        except Exception as e:
            logger.error(f"处理消息时出错: {e}")

    async def connect(self) -> bool:
        """连接到WebSocket服务器"""
        try:
            logger.info(f"正在连接到 {self.uri}...")
            self.websocket = await websockets.connect(self.uri)
            
            # 发送连接事件进行握手
            connect_event = self.create_connect_event()
            await self.websocket.send(json.dumps(connect_event))
            logger.info("连接成功，已发送握手消息")
            
            # 重置重连计数
            self.reconnect_count = 0
            
            if self.on_connect_callback:
                if asyncio.iscoroutinefunction(self.on_connect_callback):
                    await self.on_connect_callback()
                else:
                    self.on_connect_callback()
                
            return True
            
        except Exception as e:
            logger.error(f"连接失败: {e}")
            if self.on_error_callback:
                if asyncio.iscoroutinefunction(self.on_error_callback):
                    await self.on_error_callback(e)
                else:
                    self.on_error_callback(e)
            return False

    async def disconnect(self):
        """断开连接"""
        self.is_running = False
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            logger.info("连接已断开")
            
            if self.on_disconnect_callback:
                if asyncio.iscoroutinefunction(self.on_disconnect_callback):
                    await self.on_disconnect_callback()
                else:
                    self.on_disconnect_callback()

    async def run(self):
        """启动客户端主循环"""
        self.is_running = True
        
        while self.is_running:
            try:
                # 尝试连接
                if not await self.connect():
                    if self.max_reconnect_attempts > 0 and self.reconnect_count >= self.max_reconnect_attempts:
                        logger.error("达到最大重连次数，停止重连")
                        break
                    
                    self.reconnect_count += 1
                    logger.info(f"第{self.reconnect_count}次重连失败，{self.reconnect_interval}秒后重试...")
                    await asyncio.sleep(self.reconnect_interval)
                    continue
                
                # 监听消息
                async for message in self.websocket:
                    await self.handle_message(message)
                    
            except (ConnectionClosed, ConnectionClosedError):
                logger.warning("连接已关闭")
                if self.on_disconnect_callback:
                    if asyncio.iscoroutinefunction(self.on_disconnect_callback):
                        await self.on_disconnect_callback()
                    else:
                        self.on_disconnect_callback()
                    
                if self.is_running:
                    if self.max_reconnect_attempts > 0 and self.reconnect_count >= self.max_reconnect_attempts:
                        logger.error("达到最大重连次数，停止重连")
                        break
                    
                    self.reconnect_count += 1
                    logger.info(f"连接断开，{self.reconnect_interval}秒后重连... (第{self.reconnect_count}次)")
                    await asyncio.sleep(self.reconnect_interval)
                    
            except Exception as e:
                logger.error(f"运行时出错: {e}")
                if self.on_error_callback:
                    if asyncio.iscoroutinefunction(self.on_error_callback):
                        await self.on_error_callback(e)
                    else:
                        self.on_error_callback(e)
                    
                if self.is_running:
                    logger.info(f"{self.reconnect_interval}秒后重试...")
                    await asyncio.sleep(self.reconnect_interval)

    def on_message(self, callback: Callable):
        """设置消息接收回调"""
        self.on_message_callback = callback

    def on_connect(self, callback: Callable):
        """设置连接建立回调"""
        self.on_connect_callback = callback

    def on_disconnect(self, callback: Callable):
        """设置连接断开回调"""
        self.on_disconnect_callback = callback

    def on_error(self, callback: Callable):
        """设置错误回调"""
        self.on_error_callback = callback


# 示例使用
async def example_message_handler(data: Dict[str, Any]):
    """示例消息处理器"""
    logger.info(f"处理消息: {data}")

async def example_connect_handler():
    """示例连接处理器"""
    logger.info("已成功连接到服务器!")

async def example_disconnect_handler():
    """示例断线处理器"""
    logger.info("与服务器断开连接!")

async def example_error_handler(error: Exception):
    """示例错误处理器"""
    logger.error(f"发生错误: {error}")

async def main():
    """主函数示例"""
    # 创建客户端
    client = WebSocketClient(
        uri="ws://127.0.0.1:8000/ws/",
        bot_id=12345,
        reconnect_interval=5,
        max_reconnect_attempts=0  # 无限重连
    )
    
    # 设置回调函数
    client.on_message(example_message_handler)
    client.on_connect(example_connect_handler)
    client.on_disconnect(example_disconnect_handler)
    client.on_error(example_error_handler)
    
    # 启动客户端
    try:
        # 在另一个任务中运行客户端
        client_task = asyncio.create_task(client.run())
        
        # 等待一段时间后发送测试消息
        await asyncio.sleep(2)
        await client.send_text("Hello, Server!")
        
        # 等待更多时间
        await asyncio.sleep(3)
        
        # 发送心跳
        heartbeat = client.create_heartbeat_event()
        await client.send_message(heartbeat)
        
        # 保持运行
        await client_task
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在断开连接...")
        await client.disconnect()

if __name__ == "__main__":
    # 配置日志
    logger.add("ws_client.log", rotation="10 MB", level="DEBUG")
    
    # 运行客户端
    asyncio.run(main())
