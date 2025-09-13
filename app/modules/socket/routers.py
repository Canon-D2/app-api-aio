from fastapi import APIRouter, WebSocket
from .controllers import ChatController


router = APIRouter(prefix="/chat", tags=["chat"])
controller = ChatController()


@router.websocket("/ws/{channel_id}")
async def websocket_endpoint(channel_id: str, websocket: WebSocket):
    await controller.websocket_endpoint(channel_id, websocket)