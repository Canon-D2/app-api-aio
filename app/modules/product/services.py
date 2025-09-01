from bson import ObjectId
from app.mongo.base import BaseCRUD
from .exception import ErrorCode
from app.mongo.engine import engine_aio


product_crud = BaseCRUD("products", engine_aio)

class ProductServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud
    
    async def create(self, data: dict):
        result = await self.crud.create(data)
        return result

    async def update(self, _id, data):
        result = await self.crud.update_by_id(_id, data)
        return result

    async def get(self, _id):
        result = await self.crud.get_by_id(_id)
        return result

    async def delete(self, _id):
        result = await self.crud.delete_by_id(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result


    async def add_serial(self, product_id: str, number: str, status: str):
        product = await self.crud.get_by_id(product_id)
        if not product:
            raise ErrorCode.InvalidProductId()
        
        for s in product.get("serial", []):
            if s["number"] == number:
                raise ErrorCode.SerialAlreadyExists()

        payload = {"$push": {"serial": {"number": number, "status": status}}}
        await self.crud.collection.update_one({"_id": ObjectId(product_id)}, payload)
        return {"status": "success", "message": f"Serial {number} added successfully"}


    async def update_serial(self, product_id: str, number_old: str, number_new: str, status_new: str):
        product = await self.crud.get_by_id(product_id)
        if not product:
            raise ErrorCode.InvalidProductId()
        
        found = False
        for s in product.get("serial", []):
            if s["number"] == number_old:
                found = True
                break
        if not found:
            raise ErrorCode.SerialNotFound()

        payload = {
            "$set": {
                "serial.$[elem].number": number_new,
                "serial.$[elem].status": status_new
            }
        }
        array_filters = [{"elem.number": number_old}]
        await self.crud.collection.update_one({"_id": ObjectId(product_id)}, payload, array_filters=array_filters)
        return {"status": "success", "message": f"Serial {number_old} updated to {number_new}"}


    async def delete_serial(self, product_id: str, number: str):
        product = await self.crud.get_by_id(product_id)
        if not product:
            raise ErrorCode.InvalidProductId()
        
        found = False
        for s in product.get("serial", []):
            if s["number"] == number:
                found = True
                break
        if not found:
            raise ErrorCode.SerialNotFound()

        payload = {"$pull": {"serial": {"number": number}}}
        await self.crud.collection.update_one({"_id": ObjectId(product_id)}, payload)
        return {"status": "success", "message": f"Serial {number} deleted successfully"}