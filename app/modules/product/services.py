from app.db.base import BaseCRUD
from app.db.engine import engine_aio


product_crud = BaseCRUD("products", engine_aio)

class ProductServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud
    
    async def create(self, data: dict):
        result = await self.crud.create(data)
        return result

    async def update(self, _id, data):
        result = await self.service.update(_id, data)
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