from fastapi import APIRouter, Path, Query
from . import schemas
from typing import Optional
from .exception import ErrorCode
from .controllers import ProductController

router = APIRouter(prefix="/v1/products", tags=["products"])
controller = ProductController()


@router.post("", status_code=201, responses={
                201: {"model": schemas.ProductResponse, "description": "Create items success"}})
async def create_product(data: schemas.ProductCreate):
    result = await controller.create(data.model_dump())
    return schemas.ProductResponse(**result)

@router.get("/{product_id}", status_code=200, responses={
                200: {"model": schemas.ProductResponse, "description": "Get items success"}})
async def get_product(product_id: str = Path(...)):
    result = await controller.get(product_id)
    if not result:
        raise ErrorCode.InvalidProductId()
    return result

@router.put("/{product_id}", status_code=200, responses={
                200: {"model": schemas.ProductResponse, "description": "Edit items success"}})
async def update_product(product_id: str, data: schemas.ProductUpdate):
    result = await controller.update(product_id, data.model_dump(exclude_unset=True))
    return schemas.ProductResponse(**result)

@router.delete("/{product_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_user(product_id: str):
    result = await controller.delete(product_id)
    return result

@router.get("", status_code=200, responses={
                200: {"model": schemas.PaginatedProductResponse, "description": "Get items success"}})
async def list_products(
    page: int = Query(1, gt=0, description="Số trang"),
    limit: int = Query(10, le=100, description="Số item trên mỗi trang"),
    name: Optional[str] = Query(None, description="Lọc theo tên"),
    category: Optional[str] = Query(None, description="Lọc theo loại"),
    brand: Optional[str] = Query(None, description="Lọc theo thương hiệu"),
    price_min: Optional[float] = Query(None, description="Lọc sản phẩm >= giá này"),
    price_max: Optional[float] = Query(None, description="Lọc sản phẩm <= giá này"),
):
    query = {}
    if name: query["name"] = {"$regex": name, "$options": "i"}
    if category: query["category"] = {"$regex": category, "$options": "i"}
    if brand: query["brand"] = {"$regex": brand, "$options": "i"}
    if price_min is not None or price_max is not None:
        query["price"] = {k: v for k, v in (("$gte", price_min), ("$lte", price_max)) if v is not None}

    result = await controller.search(query, page, limit)
    return result