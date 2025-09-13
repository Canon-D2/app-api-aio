from pydantic import BaseModel
from typing import Literal, Optional, List


class MessageSend(BaseModel):
    content: str
    type: Literal["text", "png", "jpg", "mp3", "mp4", "pdf", "doc", "docx"]


class ChatMessages(BaseModel):
    channel_id: str
    sender: str
    content: str
    type: Literal["text", "png", "jpg", "mp3", "mp4", "pdf" ,"doc", "docx"]
    status: Literal["sending", "sent", "error"]
    created_at: float

class LastMessenge(BaseModel):
    sender: str
    content: str

class ChatChannels(BaseModel):
    members: List[str]
    last_message: Optional[LastMessenge] = None
    created_at: float
    updated_at: Optional[float] = None
