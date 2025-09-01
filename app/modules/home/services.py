from app.mongo.engine import engine_aio


class HomeService:
    async def export_bson(self) -> dict[str, list[dict]]:
        collections_data = {}
        collections = await engine_aio.list_collection_names()
        for collection_name in collections:
            collection = engine_aio.get_collection(collection_name)
            documents = []
            async with collection.find({}) as cursor:
                async for doc in cursor:
                    documents.append(doc)
            collections_data[collection_name] = documents
        return collections_data
    