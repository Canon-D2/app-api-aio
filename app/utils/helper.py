import time, datetime
import unicodedata, re

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
    
    @staticmethod
    def convert_slug(text: str) -> str:
        """Convert a string with accents and special characters into a URL-friendly slug"""
        # Normalize unicode to remove accents (e.g., é -> e, ư -> u)
        text = unicodedata.normalize("NFD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        text = text.lower()
        
        # Replace non-alphanumeric characters with hyphens
        text = re.sub(r"[^a-z0-9]+", "-", text)
        
        # Remove leading/trailing hyphens
        text = text.strip("-")
        
        return text

    @staticmethod
    def timestamp_to_date(ts: float, fmt: str = "%d-%m-%Y %H:%M:%S") -> str:
        """
        Convert timestamp (e.g., 1755688756) to date string "20-08-2025 22:59:16"
        """
        return datetime.datetime.fromtimestamp(float(ts)).strftime(fmt)

    @staticmethod
    def date_to_timestamp(date_str: str, fmt: str = "%d-%m-%Y %H:%M:%S") -> float:
        """
        Convert date string "20-08-2025 22:59:16" to timestamp (e.g., 1755688756.0)
        """
        dt = datetime.datetime.strptime(date_str, fmt)
        return dt.timestamp()