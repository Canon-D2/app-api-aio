from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from .exception import ErrorCode

cron_crud = BaseCRUD("cronjobs", engine_aio)


class CronServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud

    async def create(self, data: dict):
        result = await self.crud.create(data)
        return result

    async def update(self, _id: str, data: dict):
        result = await self.crud.update_by_id(_id, data)
        if not result: 
            raise ErrorCode.InvalidCronId()
        return result
    
    async def get(self, _id):
        result = await self.crud.get_by_id(_id)
        if not result: 
            raise ErrorCode.InvalidCronId()
        return result

    async def delete(self, _id):
        result = await self.crud.delete_by_id(_id)
        if not result: 
            raise ErrorCode.InvalidCronId()
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result
