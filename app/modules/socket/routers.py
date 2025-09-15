from fastapi import APIRouter, WebSocket
from .controllers import ChatController

router = APIRouter(prefix="/chat", tags=["chat"])
controller = ChatController()

@router.websocket("/ws/{channel_id}")
async def chat_realtime(channel_id: str, websocket: WebSocket):
    await controller.chat_realtime(channel_id, websocket)