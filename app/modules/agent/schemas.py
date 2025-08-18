from typing import Optional
from pydantic import BaseModel, Field

class GeminiRequest(BaseModel):
    prompt: Optional[str] = None
    content: str
    model: str = Field(default="gemini-2.5-flash-lite")

class OpenAIRequest(BaseModel):
    prompt: Optional[str] = None
    content: str
    model: str = Field(default="gpt-4o-mini")

class Response(BaseModel):
    generate: str