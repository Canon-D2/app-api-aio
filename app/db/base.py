import math
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from app.utils.helper import Helper

class BaseCRUD:
    def __init__(self, collection_name: str, db) -> None:
        self.db = db
        self.collection = db[collection_name]

    async def create(self, data: dict):
        data["created_at"] = Helper.get_timestamp()
        user = await self.collection.insert_one(data)
        result = await self.collection.find_one({"_id": user.inserted_id})
        result = Helper.convert_object_id(result)
        return result

    async def get_by_id(self, _id: str):
        result = await self.collection.find_one({"_id": ObjectId(_id)})
        result = Helper.convert_object_id(result) if result else None 
        return result

    async def update_by_id(self, _id: str, data: dict):
        data["updated_at"] = Helper.get_timestamp()
        await self.collection.update_one(
            {"_id": ObjectId(_id)}, {"$set": data}
        )
        result = await self.collection.find_one({"_id": ObjectId(_id)})
        result = Helper.convert_object_id(result)
        return result

    async def delete_by_id(self, _id: str):
        result = await self.collection.delete_one({"_id": ObjectId(_id)})
        result = {"status": "success"} if result.deleted_count > 0 else {"status": "failed"}
        return result

    async def search(
        self,
        query: dict = {},
        page: int = 1,
        limit: int = 10,
        sort_field: str = "created_at",
        is_desc: bool = True,
    ):
        skip = (page - 1) * limit
        cursor = (
            self.collection.find(query)
            .sort(self._get_sort(sort_field, is_desc))
            .skip(skip)
            .limit(limit)
        )
        results = [Helper.convert_object_id(doc) async for doc in cursor]
        total = await self.collection.count_documents(query)
        result =  {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": math.ceil(total / limit),
            "results": results,
        }
        return result
    
    async def get_one(self, query: dict):
        result = await self.collection.find_one(query)
        return result
    
    async def update_one(self, query: dict, data: dict):
        data["updated_at"] = Helper.get_timestamp()
        await self.collection.update_one(query, data)
        
        result = await self.collection.find_one(query)
        result = Helper.convert_object_id(result) if result else None
        return result
    
    async def find_one(self, query: dict):
        result = await self.collection.find_one(query)
        result =  Helper.convert_object_id(result) if result else None
        return result
    
    def _get_sort(self, sort_field: str, is_desc: bool):
        result = [(sort_field, DESCENDING if is_desc else ASCENDING)]
        return result
