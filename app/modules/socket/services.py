from typing import Dict, Tuple
from . import schemas
from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.utils.helper import Helper
from .exception import ErrorCode

channels_crud = BaseCRUD("chat-channels", engine_aio)
messages_crud = BaseCRUD("chat-messages", engine_aio)


class ChatServices:
    def __init__(self, channels_crud: BaseCRUD, messages_crud: BaseCRUD):
        self.channels_crud = channels_crud
        self.messages_crud = messages_crud
        self.active_connections: Dict[str, list[Tuple[any, str]]] = {}

    async def _validate_user_in_channel(self, channel_id: str, token: str):
        try:
            payload = await Helper.decode_access_token(token)
            user_id = payload.get("uid")
        except Exception:
            raise ErrorCode.UserNotFound()

        channel = await self.channels_crud.get_by_id(channel_id)
        if not channel:
            raise ErrorCode.ChannelNotFound()

        if user_id not in channel.get("members", []):
            raise ErrorCode.UserNotFound()

        return user_id, channel

    async def connect(self, channel_id: str, websocket, token: str):
        # Validate & add connect in list
        user_id, _ = await self._validate_user_in_channel(channel_id, token)
        await websocket.accept()
        self.active_connections.setdefault(channel_id, []).append((websocket, user_id))

    def disconnect(self, channel_id: str, websocket):
        # Delete connect WebSocket
        if channel_id in self.active_connections:
            self.active_connections[channel_id] = [
                (ws, uid) for (ws, uid) in self.active_connections[channel_id] if ws != websocket
            ]
            if not self.active_connections[channel_id]:
                del self.active_connections[channel_id]

    async def broadcast(self, channel_id: str, message: dict, members: list):
        # Send message to all websocket for member
        for ws, uid in self.active_connections.get(channel_id, []).copy():
            if uid not in members:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                self.active_connections[channel_id].remove((ws, uid))

    async def send_message(self, data: dict, token: str) -> dict:
        sender_id, channel = await self._validate_user_in_channel(data["channel_id"], token)

        chat_message = schemas.ChatMessages(
            channel_id=data["channel_id"],
            sender=sender_id,
            content=data["content"],
            type=data.get("type", "text"),
            status="sent",
            created_at=Helper.get_timestamp(),
        )
        await self.messages_crud.create(chat_message.dict())

        last_message = schemas.LastMessenge(sender=sender_id, content=data["content"])
        await self.channels_crud.update_by_id(channel["_id"], {"last_message": last_message.dict()})

        await self.broadcast(data["channel_id"], chat_message.dict(), channel["members"])
        return chat_message.dict()


socket_service = ChatServices(channels_crud, messages_crud)
