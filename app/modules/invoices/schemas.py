from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class InvoiceUpdate(BaseModel):
    address: Optional[str] = None
    note: Optional[str] = None
    type_vat: Optional[Literal["company", "person", "b2b"]] = None
    status: Optional[Literal["pending", "confirmed", "shipped", "delivered", "cancelled", "failed"]] = None


class InvoiceItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    image: Optional[str] = None


class InvoiceResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    items: List[InvoiceItem]
    address: Optional[str]
    note: Optional[str]
    total_items: int
    total_price: float
    type_vat: Optional[str]
    status: str
    created_at: datetime


class PaginatedInvoiceResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[InvoiceResponse]
