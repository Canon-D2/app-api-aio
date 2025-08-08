from .services import user_crud, UserServices


class UserController:
    def __init__(self):
        self.crud = user_crud
        self.service = UserServices(self.crud)

    async def create(self, data):
        return await self.service.create(data)

    async def update(self, _id, data):
        return await self.service.update(_id, data)

    async def get_by_id(self, _id):
        return await self.crud.get_by_id(_id)

    async def delete(self, _id):
        return await self.crud.delete_by_id(_id)

    async def search(self, query: dict, page: int, limit: int):
        return await self.crud.search(query, page, limit)
