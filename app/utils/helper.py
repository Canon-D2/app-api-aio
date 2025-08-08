import time, datetime

class Helper:
    @staticmethod
    def get_timestamp() -> float:
        return time.time()

    @staticmethod
    def convert_object_id(doc: dict) -> dict:
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @staticmethod
    async def is_email_exists(crud, email: str, exclude_id: str = None) -> bool:
        if not email:
            return False
        query = {"email": email}
        if exclude_id:
            from bson import ObjectId
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        existing = await crud.collection.find_one(query)
        return existing is not None
    
    @staticmethod
    def get_future_timestamp(days_to_add: int) -> float:
        current_date = datetime.datetime.now()
        future_date = current_date + datetime.timedelta(days=days_to_add)
        return future_date.timestamp() 