from decimal import Decimal
from bson.decimal128 import Decimal128
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal


class TicketType(BaseModel):
    type: Literal["vip", "base"]
    quantity: int
    sold: int = 0
    price: float


class EventCreate(BaseModel):
    name: str
    date: int
    location: str
    types: List[TicketType]
    total_tickets: int


class EventUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[int] = None
    location: Optional[str] = None
    types: Optional[List[TicketType]] = None
    total_tickets: Optional[int] = None


class EventResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    date: int
    location: str
    types: List[TicketType]
    total_tickets: int

class PaginatedEventResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[EventResponse]


class CheckoutTicket(BaseModel):
    type: str
    quantity: int


class CheckoutRequest(BaseModel):
    event_id: str
    user_id: str
    tickets: List[CheckoutTicket]
    

class CheckinRequest(BaseModel):
    qr_token: str
    check_by: str


class TicketResponse(BaseModel):
    id: str = Field(alias="_id")
    event_id: str
    user_id: str
    type: str
    price: Decimal
    status: Literal["paid", "pending", "canceled"]
    qr_token: str
    check_in: Optional[int] = None
    check_by: Optional[str] = None

    @validator('price')
    def convert_decimal(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v


class PaginatedTicketResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[TicketResponse]