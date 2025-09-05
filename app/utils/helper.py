from bson import ObjectId
from jose import jwt
import unicodedata, re
import time, datetime, random, string
from app.auth.config import SECRET_KEY, ALGORITHM

class Helper:
    
    @staticmethod
    def _key(user_id: str) -> str:
        return f"cart:{user_id}"
    
    @staticmethod
    def _recalc(cart: dict) -> dict:
        total_items = sum(it.quantity for it in cart.items)
        total_price = sum(it.price * it.quantity for it in cart.items)
        cart.total_items = total_items
        cart.total_price = total_price
        cart.last_update = Helper.get_timestamp()
        return cart
    
    @staticmethod
    def get_timestamp() -> float:
        timestamp = time.time()
        return timestamp

    @staticmethod
    def convert_object_id(doc: dict) -> dict:
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc
    
    @staticmethod
    def is_object_id(id: str) -> bool:
        try:
            ObjectId(id)
            return True
        except Exception:
            return False

    @staticmethod
    async def is_email_exists(crud, email: str, exclude_id: str = None) -> bool:
        if not email:
            return False
        query = {"email": email}
        if exclude_id:
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
        # Convert timestamp (e.g., 1755688756) to date string "20-08-2025 22:59:16"
        result = datetime.datetime.fromtimestamp(float(ts)).strftime(fmt)
        return result

    @staticmethod
    def date_to_timestamp(date_str: str, fmt: str = "%d-%m-%Y %H:%M:%S") -> float:
        # Convert date string "20-08-2025 22:59:16" to timestamp (e.g., 1755688756.0)
        dt = datetime.datetime.strptime(date_str, fmt)
        return dt.timestamp()
    
    @staticmethod
    def generate_ticket_code():
        # Generate ticket code of first 5 letters + 12 random numbers, for example LYPJR714855620195
        prefix = ''.join(random.choices(string.ascii_uppercase, k=5))
        number = ''.join(random.choices(string.digits, k=12))
        return f"{prefix}{number}"
    
    @staticmethod
    async def decode_access_token(data: str):
        decode = jwt.decode(token=data, key=SECRET_KEY, algorithms=[ALGORITHM])
        return decode