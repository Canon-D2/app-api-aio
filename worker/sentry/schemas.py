from pydantic import BaseModel
from typing import Optional


class Response(BaseModel):
    issues_link: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
    title: Optional[str] = None
    function: Optional[str] = None
    filename: Optional[str] = None
    context_line: Optional[str] = None
