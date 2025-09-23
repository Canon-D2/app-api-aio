from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    image: Optional[str] = None


class CartResponse(BaseModel):
    user_id: str
    items: List[CartItem] = Field(default_factory=list)
    address: Optional[str] = None
    note: Optional[str] = None
    total_items: int = 0
    total_price: float = 0.0
    last_update: Optional[float] = None 
    type_vat: Optional[Literal["company", "person", "b2b"]] = None


class AddCart(BaseModel):
    item: CartItem
    address: Optional[str] = None
    note: Optional[str] = None
    type_vat: Literal["company", "person", "b2b"]


class EditCart(BaseModel):
    product_id: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    image: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = None
    type_vat: Optional[Literal["company", "person", "b2b"]] = None


class DeleteCart(BaseModel):
    product_id: Optional[str] = None