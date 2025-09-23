from . import schemas
from fastapi import APIRouter
from .controllers import CartController


router = APIRouter(prefix="/v1/cart", tags=["redis-cart"])
controller = CartController()


@router.post("/add/{user_id}", status_code=201, responses={
                201: {"model": schemas.CartResponse, "description": "Add items success"}})
async def add_cart(user_id: str, data: schemas.AddCart):
    result = await controller.add_cart(user_id, data)
    return result


@router.put("/edit/{user_id}", status_code=200, responses={
                200: {"model": schemas.CartResponse, "description": "Edit items success"}})
async def edit_cart(user_id: str, data: schemas.EditCart):
    result = await controller.edit_cart(user_id, data)
    return result


@router.delete("/delete/{user_id}", status_code=200, responses={
                200: {"model": schemas.CartResponse, "description": "Delete items success"}})
async def delete_cart(user_id: str, data: schemas.DeleteCart):
    result = await controller.delete_cart(user_id, data)
    return result


@router.get("/get/{user_id}", status_code=200, responses={
                200: {"model": schemas.CartResponse, "description": "Get items success"}})
async def get_cart(user_id: str):
    result = await controller.get_cart(user_id)
    return result
