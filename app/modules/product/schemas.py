from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ProductDescription(BaseModel):
    title: Optional[str] = None
    link: str
    content: str


class ProductCreate(BaseModel):
    sku: str
    serial: List[str]
    name: str
    category: str
    brand: str
    status: str
    quantity: int
    price: float
    images: List[str]
    tags: List[str]
    specs: Optional[Dict[str, Any]] = None 
    desc: List[ProductDescription]
    create_at: Optional[float] = None
    update_at: Optional[float] = None


class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    serial: Optional[List[str]] = None
    name: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    status: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    specs: Optional[Dict[str, Any]] = None 
    desc: Optional[List[ProductDescription]] = None
    update_at: Optional[float] = None


class ProductResponse(BaseModel):
    id: str = Field(alias="_id")
    sku: str
    serial: List[str]
    name: str
    category: str
    brand: str
    status: str
    quantity: int
    price: float
    images: List[str]
    tags: List[str]
    specs: Optional[Dict[str, Any]] = None
    desc: List[ProductDescription]
    create_at: Optional[float]
    update_at: Optional[float]


class PaginatedProductResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[ProductResponse]
