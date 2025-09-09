from jose import jwt
import unicodedata, re
from io import BytesIO
from bson import ObjectId
from fastapi import Response
from zoneinfo import ZoneInfo
from typing import Literal, Optional
import time, datetime, random, string, secrets, base64, qrcode
from app.auth.config import SECRET_KEY, ALGORITHM

class Helper:
    
    @staticmethod
    def _key(user_id: str) -> str:
        result = f"cart:{user_id}"
        return result
    
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
    def object_to_string(doc: dict) -> dict:
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc
    
    @staticmethod
    def string_to_object(query: dict) -> dict:
        if "_id" in query and isinstance(query["_id"], str) and Helper.is_object_id(query["_id"]):
            query["_id"] = ObjectId(query["_id"])
        return query
    
    @staticmethod
    def is_object_id(_id: str) -> bool:
        result =  ObjectId.is_valid(_id)
        return result

    @staticmethod
    async def is_email_exists(crud, email: str, exclude_id: str = None) -> bool:
        if not email: 
            return False
        query = {"email": email}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        existing = await crud.get_one_query(query=query)
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
    def timestamp_to_date(ts: float, fmt: str = "%d-%m-%Y %H:%M:%S", tz: Optional[str] = "Asia/Ho_Chi_Minh") -> str:
        # Convert timestamp (e.g., 1755688756) to date string "20-08-2025 22:59:16"
        # Timezone ex: Asia/Tokyo, None, UTC,...
        result = datetime.datetime.fromtimestamp(float(ts), tz=ZoneInfo(tz))
        return result.strftime(fmt)

    @staticmethod
    def date_to_timestamp(date_str: str, fmt: str = "%d-%m-%Y %H:%M:%S", tz: Optional[str] = "Asia/Ho_Chi_Minh") -> float:
        # Convert date string "20-08-2025 22:59:16" to timestamp (e.g., 1755688756.0)
        result = datetime.datetime.strptime(date_str, fmt)
        result = result.replace(tzinfo=ZoneInfo(tz))
        return result.timestamp()
    
    @staticmethod
    def generate_ticket_code() -> str:
        # Generate ticket code of first 5 letters + 12 random numbers, for example LYPJR714855620195
        prefix = ''.join(random.choices(string.ascii_uppercase, k=5))
        number = ''.join(random.choices(string.digits, k=12))
        return f"{prefix}{number}"
    
    @staticmethod
    async def decode_access_token(token: str) -> dict:
        result = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return result
    
    @staticmethod
    def generate_secret_otp(length: int = 6) -> str:
        chars = string.ascii_uppercase + string.digits
        while True:
            otp_code = ''.join(secrets.choice(chars) for _ in range(length))
            if sum(c.isalpha() for c in otp_code) >= 2 and sum(c.isdigit() for c in otp_code) >= 2:
                return otp_code
            
    @staticmethod
    def generate_qr_code(data: str, format: Literal["base64", "image"]):
        qr = qrcode.make(data)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        image_bytes = buf.getvalue()

        if format == "base64":
            b64 = base64.b64encode(image_bytes).decode("utf-8")
            result = {"data": data,"qr_code": f"data:image/png;base64,{b64}"}
        else:
            result = Response(
                content=image_bytes, 
                media_type="image/png", 
                # headers={"Content-Disposition": f"attachment; filename=qr_{data}.png"} # Download
                )
        return result