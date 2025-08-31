from typing import Any, Dict
from app.db.base import BaseCRUD
from app.db.engine import engine_aio
from .exception import ErrorCode
from app.modules.user.services import user_crud

thread_crud = BaseCRUD("forum-threads", engine_aio)
post_crud = BaseCRUD("forum-posts", engine_aio)


class ThreadServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud

    async def create(self, data: dict):
        user = await user_crud.get_by_id(data["author_id"])
        
        if not user: return ErrorCode.UserNotFound()

        result = await self.crud.create(data)
        return result

    async def get(self, _id: str):  
        result = await self.crud.get_by_id(_id)
        return result

    async def update(self, _id: str, data: dict):
        result = await self.crud.update_by_id(_id, data)
        return result

    async def delete(self, _id: str):
        result = await self.crud.delete_by_id(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result


class PostServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud

    async def create(self, data: dict):

        thread = await thread_crud.get_by_id(data["thread_id"])
        user = await user_crud.get_by_id(data["author"]["user_id"])

        if not thread: return ErrorCode.ThreadNotFound()
        if not user: return ErrorCode.UserNotFound()

        await thread_crud.update_by_id(thread["_id"], {"$inc": {"comments": 1}})

        result = await self.crud.create(data)
        return result

    async def get(self, _id: str):
        result = await self.crud.get_by_id(_id)
        return result

    async def update(self, _id: str, data: dict):
        result = await self.crud.update_by_id(_id, data)
        return result

    async def delete(self, _id: str):

        post = await self.crud.get_by_id(_id)
        if not post: raise ErrorCode.PostNotFound()

        thread = await thread_crud.get_by_id(post.get("thread_id"))
        if thread: 
            await thread_crud.update_by_id(thread["_id"], {"$inc": {"comments": -1}})

        result = await self.crud.delete_by_id(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result

    async def reaction(self, post_id: str, reaction: str, user_id: str) -> Dict[str, Any]:
        post = await self.crud.get_by_id(post_id)
        if not post:
            raise ErrorCode.PostNotFound()

        reactions = post.get("reactions", {})

        # Check exist Reaction for User
        user_already_reacted = user_id in reactions.get(reaction, [])

        # If again reaction -> Remove
        if user_already_reacted:
            reactions[reaction].remove(user_id)
            
            # Delete Reaction empty
            # if not reactions[reaction]:
                # del reactions[reaction]
        else:
            # Delete reaction old and add reaction new
            for rtype, users in reactions.items():
                if user_id in users:
                    reactions[rtype].remove(user_id)

            reactions.setdefault(reaction, []).append(user_id)

        await self.crud.update_by_id(str(post["_id"]), {"reactions": reactions})
        return {"post_id": post_id, "reactions": reactions}
