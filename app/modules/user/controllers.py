from .services import user_crud, UserServices


class UserController:
    def __init__(self):
        self.crud = user_crud
        self.service = UserServices(self.crud)

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
