from fastapi import WebSocket
from . import schemas
from .services import chat_service


class ChatController:
    def __init__(self):
        self.service = chat_service

    async def websocket_endpoint(self, channel_id: str, websocket: WebSocket):
        token = websocket.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return await websocket.close()

        try:
            await self.service.connect(channel_id, websocket, token)
            while True:
                data = schemas.MessageSend(**await websocket.receive_json())
                await self.service.send_message({"channel_id": channel_id, **data.dict()}, token)
        except Exception:
            print("[CONTROLLER] - Websocket Close")
            await websocket.close()
        finally:
            self.service.disconnect(channel_id, websocket)
