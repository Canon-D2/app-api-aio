from decimal import Decimal
from bson.decimal128 import Decimal128
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, validator


class InvoiceUpdate(BaseModel):
    address: Optional[str] = None
    note: Optional[str] = None
    type_vat: Optional[Literal["company", "person", "b2b"]] = None
    status: Optional[Literal["pending", "confirmed", "shipped", "delivered", "cancelled", "failed"]] = None


class InvoiceItem(BaseModel):
    product_id: str
    name: str
    price: Decimal
    quantity: int
    image: Optional[str] = None

    @validator('price')
    def convert_decimal(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v


class InvoiceResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    items: List[InvoiceItem]
    address: Optional[str]
    note: Optional[str]
    total_items: int
    total_price: Decimal
    type_vat: Optional[str]
    status: str
    created_at: float

    @validator('total_price')
    def convert_decimal(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v



class PaginatedInvoiceResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[InvoiceResponse]


class ItemEmail(BaseModel):
    name: str
    price: float
    quantity: int
    image: Optional[str] = None


class InvoiceEmail(BaseModel):
    items: List[ItemEmail]
    address: Optional[str]
    note: Optional[str]
    total_items: int
    total_price: float