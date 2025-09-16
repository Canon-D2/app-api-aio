from decimal import Decimal
from bson.decimal128 import Decimal128
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal

class SerialItem(BaseModel):
    number: str
    status: Literal["available", "faulty", "in-transit", "ordered"]


class ProductDescription(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = None
    content: Optional[str] = None


class ProductCreate(BaseModel):
    name: str
    category: str
    serial: List[SerialItem] 
    brand: str
    status: Literal["in-stock", "out-of-stock", "coming-soon", "pre-order"]
    quantity: int
    price: float
    images: List[str]
    tags: List[str]
    specs: Optional[Dict[str, Any]] = None 
    theme: Optional[str] = None
    description: List[ProductDescription]


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    serial: Optional[List[SerialItem]] = None
    brand: Optional[str] = None
    status: Optional[Literal["in-stock", "out-of-stock", "coming-soon", "pre-order"]] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    specs: Optional[Dict[str, Any]] = None 
    theme: Optional[str] = None
    description: Optional[List[ProductDescription]] = None


class ProductResponse(BaseModel):
    id: str = Field(alias="_id")
    sku: str
    name: str
    category: str
    serial: List[SerialItem]
    brand: str
    status: Optional[str]
    quantity: int
    price: Decimal
    images: List[str]
    tags: List[str]
    specs: Optional[Dict[str, Any]] = None
    theme: Optional[str]
    description: List[ProductDescription]

    @validator('price')
    def convert_decimal(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v


class PaginatedProductResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[ProductResponse]


class SerialCreate(BaseModel):
    number: str
    status: Literal["available", "faulty", "in-transit", "ordered"]


class SerialUpdate(BaseModel):
    number_old: str
    number_new: str
    status_new: Literal["available", "faulty", "in-transit", "ordered"]


class SerialDelete(BaseModel):
    number: str