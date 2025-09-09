import math
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from app.utils.helper import Helper

class BaseCRUD:
    def __init__(self, collection_name: str, db) -> None:
        self.db = db
        self.collection = db[collection_name]

    async def create(self, data: dict) -> dict:
        data["created_at"] = Helper.get_timestamp()
        record = await self.collection.insert_one(data)
        result = await self.get_by_id(str(record.inserted_id))
        return result

    async def get_by_id(self, _id: str) -> dict:
        if not Helper.is_object_id(_id): return None
        result = await self.collection.find_one({"_id": ObjectId(_id)})
        result = Helper.object_to_string(result) if result else None 
        return result

    async def update_by_id(self, _id: str, data: dict) -> dict:
        if not Helper.is_object_id(_id): return None
        data["updated_at"] = Helper.get_timestamp()
        await self.collection.update_one({"_id": ObjectId(_id)}, {"$set": data})
        result = await self.get_by_id(_id)
        return result

    async def delete_by_id(self, _id: str):
        if not Helper.is_object_id(_id): return None
        result = await self.collection.delete_one({"_id": ObjectId(_id)})
        result = {"status": "success"} if result.deleted_count > 0 else {"status": "failed"}
        return result
    
    async def get_one_query(self, query: dict) -> dict:
        query = Helper.string_to_object(query) # Check query contain _id
        result = await self.collection.find_one(query)
        result =  Helper.object_to_string(result) if result else None
        return result
    
    async def update_one_query(self, query: dict, data: dict):
        query = Helper.string_to_object(query) # Check query contain _id
        data["updated_at"] = Helper.get_timestamp()
        await self.collection.update_one(query, {"$set": data})

        result = await self.get_one_query(query)
        return result

    async def update_no_limit(self, query: dict, data: dict, **kwargs):
        query = Helper.string_to_object(query) # Check query contain _id

        if not any(key.startswith("$") for key in data.keys()):
            # Case 1: Replace data if not operator
            data["updated_at"] = Helper.get_timestamp()
            await self.collection.replace_one(query, data, **kwargs)
        else:
            # Case 2: $set, $unset, $push, $pull
            if "$set" not in data:
                data["$set"] = {}
            data["$set"]["updated_at"] = Helper.get_timestamp()
            await self.collection.update_one(query, data, **kwargs)

        return await self.get_one_query(query)

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
        results = [Helper.object_to_string(doc) async for doc in cursor]
        total = await self.collection.count_documents(query)
        result =  {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": math.ceil(total / limit),
            "results": results,
        }
        return result
    
    def _get_sort(self, sort_field: str, is_desc: bool):
        result = [(sort_field, DESCENDING if is_desc else ASCENDING)]
        return result

    async def aggregate_by_pipeline(self, pipeline):
        documents = self.collection.aggregate(pipeline)
        if not documents:
            return None
        results = {}
        async for document in documents:
            results.update(document)
        return results
    
    async def update_all_query(self, query: dict, data: dict):
        query = Helper.string_to_object(query) 
        data["updated_at"] = Helper.get_timestamp()

        await self.collection.update_many(query, {"$set": data})

        cursor = self.collection.find(query)
        results = [Helper.object_to_string(doc) async for doc in cursor]
        total = len(results)

        result = {"total": total, "results": results}
        return result
    

    async def delete_all_query(self, query: dict):
        query = Helper.string_to_object(query)
        cursor = self.collection.find(query, {"_id": 1})
        ids = [str(doc["_id"]) async for doc in cursor]

        result = await self.collection.delete_many(query)
        total_deleted = result.deleted_count

        result = {"total": total_deleted,"results": ids}
        return result