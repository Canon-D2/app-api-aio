from typing import Dict, Any
from .services import CartService
from .schemas import AddCart, EditCart, DeleteCart


class CartController:
    def __init__(self):
        self.service = CartService()

    async def add_cart(self, user_id: str, data: AddCart) -> Dict[str, Any]:
        result = await self.service.add_item(user_id, data)
        return result

    async def edit_cart(self, user_id: str, data: EditCart) -> Dict[str, Any]:
        result = await self.service.edit(user_id, data)
        return result

    async def delete_cart(self, user_id: str, data: DeleteCart) -> Dict[str, Any]:
        result = await self.service.delete(user_id, data)
        return result

    async def get_cart(self, user_id: str) -> Dict[str, Any]:
        result = await self.service.get_cart(user_id)
        return result
