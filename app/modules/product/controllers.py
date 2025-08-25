from .services import product_crud, ProductServices

class ProductController:
    def __init__(self):
        self.crud = product_crud
        self.service = ProductServices(self.crud)

    async def create(self, data):
        result = await self.service.create(data)
        return result
    
    async def get(self, _id):
        result = await self.service.get(_id)
        return result
    
    async def update(self, _id, data):
        result = await self.service.update(_id, data)
        return result

    async def delete(self, _id):
        result = await self.service.delete(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result
    
    async def add_serial(self, product_id, number, status):
        result = await self.service.add_serial(product_id, number, status)
        return result

    async def update_serial(self, product_id, number_old, number_new, status_new):
        result = await self.service.update_serial(product_id, number_old, number_new, status_new)
        return result

    async def delete_serial(self, product_id, number):
        result = await self.service.delete_serial(product_id, number)
        return result
