from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.utils.helper import Helper
from . exception import ErrorCode
from worker.redis.services import CartService
from worker.telegram.services import invoice_bot


invoice_crud = BaseCRUD("invoices", engine_aio)


class InvoiceServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud
        self.cart_service = CartService()

    async def create_from_cart(self, user_id: str):
        cart = await self.cart_service.get_cart(user_id)
        if not cart:
            raise ErrorCode.CartNotFound()
        if not cart.get("items"):
            raise ErrorCode.CartEmpty()

        invoice = {
            "user_id": cart["user_id"],
            "items": cart["items"],
            "address": cart.get("address"),
            "note": cart.get("note"),
            "total_items": cart.get("total_items", 0),
            "total_price": cart.get("total_price", 0.0),
            "type_vat": cart.get("type_vat"),
            "status": "pending",
            "created_at": Helper.get_timestamp(),
        }

        result = await self.crud.create(invoice)

        await invoice_bot.send_telegram(invoice)
        await self.cart_service.redis.delete(Helper._key(user_id))

        return result

    async def update(self, _id, data: dict):
        result = await self.crud.update_by_id(_id, data)
        return result

    async def get(self, _id):
        result = await self.crud.get_by_id(_id)
        return result

    async def delete(self, _id):
        result = await self.crud.delete_by_id(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result
