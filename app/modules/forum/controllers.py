from typing import Any, Dict
from .services import thread_crud, post_crud, ThreadServices, PostServices


class ThreadController:
    def __init__(self):
        self.crud = thread_crud
        self.service = ThreadServices(self.crud)

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
    
    async def search(self, query, page, limit): 
        result = await self.service.search(query, page, limit)
        return result


class PostController:
    def __init__(self):
        self.crud = post_crud
        self.service = PostServices(self.crud)

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

    async def search(self, query, page, limit): 
        result = await self.service.search(query, page, limit)
        return result

    async def reaction(self, post_id: str, reaction: str, user_id: str) -> Dict[str, Any]:
        result = await self.service.reaction(post_id, reaction, user_id)
        return result