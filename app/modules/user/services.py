from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.utils.helper import Helper
from .exception import ErrorCode
from app.auth.services import auth_services

user_crud = BaseCRUD("users", engine_aio)


class UserServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud

    async def create(self, data: dict):
        email = data.get("email")
        if await Helper.is_email_exists(self.crud, email):
            raise ErrorCode.EmailExisted(email)
        
        if data.get("password"):
            data["password"] = (await auth_services.hash_password(data["password"])).decode()

        return await self.crud.create(data)

    async def update(self, _id: str, data: dict):
        email = data.get("email")
        if email and await Helper.is_email_exists(self.crud, email, exclude_id=_id):
            raise ErrorCode.InvalidUserId
        
        if data.get("password"):
            data["password"] = (await auth_services.hash_password(data["password"])).decode()

        return await self.crud.update_by_id(_id, data)
    
    async def get(self, _id):
        result = await self.crud.get_by_id(_id)
        return result

    async def delete(self, _id):
        result = await self.crud.delete_by_id(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result
