from fastapi import APIRouter, Path, Query
from . import schemas
from typing import Optional
from .controllers import ProductController

router = APIRouter(prefix="/v1/product", tags=["product"])
controller = ProductController()


@router.post("/create", status_code=201, responses={
                201: {"model": schemas.ProductResponse, "description": "Create items success"}})
async def create_product(data: schemas.ProductCreate):
    result = await controller.create(data.model_dump())
    return schemas.ProductResponse(**result)

@router.get("/get/{product_id}", status_code=200, responses={
                200: {"model": schemas.ProductResponse, "description": "Get items success"}})
async def get_product(product_id: str = Path(...)):
    result = await controller.get(product_id)
    return result

@router.put("/edit/{product_id}", status_code=200, responses={
                200: {"model": schemas.ProductResponse, "description": "Edit items success"}})
async def update_product(product_id: str, data: schemas.ProductUpdate):
    result = await controller.update(product_id, data.model_dump(exclude_unset=True))
    return schemas.ProductResponse(**result)

@router.delete("/delete/{product_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_product(product_id: str):
    result = await controller.delete(product_id)
    return result

@router.get("/search", status_code=200, responses={
                200: {"model": schemas.PaginatedProductResponse, "description": "Get items success"}})
async def list_products(
    page: int = Query(1, gt=0, description="Số trang"),
    limit: int = Query(10, le=100, description="Số item / mỗi trang"),
    name: Optional[str] = Query(None, description="Tìm theo tên"),
    category: Optional[str] = Query(None, description="Tìm theo loại"),
    brand: Optional[str] = Query(None, description="Tìm theo hãng"),
    price_min: Optional[float] = Query(None, description="Lọc sản phẩm >= giá này"),
    price_max: Optional[float] = Query(None, description="Lọc sản phẩm <= giá này"),
    series: Optional[str] = Query(None, description="Tìm nhiều serial, Ex: IP15PM-00001,IP15PM-,..."),
):
    query = {}
    if name: query["name"] = {"$regex": name, "$options": "i"}
    if category: query["category"] = {"$regex": category, "$options": "i"}
    if brand: query["brand"] = {"$regex": brand, "$options": "i"}
    if price_min is not None or price_max is not None:
        query["price"] = {k: v for k, v in (("$gte", price_min), ("$lte", price_max)) if v is not None}
    if series:
        series_list = [s.strip() for s in series.split(",") if s.strip()]
        if series_list:
            query["serial.number"] = {"$in": series_list}

    result = await controller.search(query, page, limit)
    return result

@router.post("/serials/add/{product_id}", status_code=200, responses={
                200: {"description": "Create items success"}})
async def add_serial(product_id: str, data: schemas.SerialCreate):
    result = await controller.add_serial(product_id, data.number, data.status)
    return result

@router.put("/serials/edit/{product_id}", status_code=200, responses={
                200: {"description": "Edit items success"}})
async def update_serial(product_id: str, data: schemas.SerialUpdate):
    result = await controller.update_serial(product_id, data.number_old, data.number_new, data.status_new)
    return result

@router.delete("/serials/delete/{product_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_serial(product_id: str, data: schemas.SerialDelete):
    result = await controller.delete_serial(product_id, data.number)
    return result