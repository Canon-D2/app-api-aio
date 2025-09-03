from .services import invoice_crud, InvoiceServices


class InvoiceController:
    def __init__(self):
        self.crud = invoice_crud
        self.service = InvoiceServices(self.crud)

    async def checkout_cart(self, user_id: str):
        result = await self.service.checkout_cart(user_id)
        return result

    async def get(self, _id: str):
        result = await self.service.get(_id)
        return result

    async def update(self, _id: str, data: dict):
        result = await self.service.update(_id, data)
        return result

    async def delete(self, _id: str):
        result = await self.service.delete(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result
