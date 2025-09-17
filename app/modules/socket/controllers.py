from fastapi import WebSocket, WebSocketDisconnect
from . import schemas
from .services import socket_service
from worker.kafka.controllers import kafka_controller


class ChatController:
    def __init__(self):
        self.service = socket_service

    async def chat_realtime(self, channel_id: str, websocket: WebSocket):

        token = websocket.headers.get("Authorization", "").replace("Bearer ", "")
        if not token: return await websocket.close()

        try:
            await self.service.connect(channel_id, websocket, token)
            while True:
                data = schemas.MessageSend(**await websocket.receive_json())
                # await self.service.send_message({"channel_id": channel_id, **data.dict()}, token) # Send direct
                await kafka_controller.publish_message(channel_id=channel_id, token=token, message={**data.dict()})

        except WebSocketDisconnect:
            print(f"[CONTROLLER] - Client disconnected from {channel_id}")
            
        except Exception as e:
            print(f"[CONTROLLER] - Websocket Close: {e}")
            await websocket.close()

        finally: # Clear memory socket connecting
            self.service.disconnect(channel_id, websocket)
