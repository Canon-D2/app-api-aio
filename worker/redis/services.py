import json
from typing import Optional, Dict, Any, List

from redis.asyncio import Redis
from redis.exceptions import RedisError

from .schemas import CartResponse, CartItem, AddCart, EditCart, DeleteCart
from .config import REDIS_URL
from .exception import ErrorCode
from app.utils.helper import Helper


class CartService:
    def __init__(self, redis_url: str = REDIS_URL):
        self.redis: Redis = Redis.from_url(redis_url, decode_responses=True)

    async def _load_cart(self, user_id: str, required: bool = False) -> Optional[CartResponse]:
        try:
            data = await self.redis.get(Helper._key(user_id))
        except RedisError as e:
            raise ErrorCode.GeneralError(str(e))

        if not data:
            if required:
                raise ErrorCode.ItemNotFound()
            return None

        obj = json.loads(data)
        items = [CartItem(**it) for it in obj.get("items", [])]
        return CartResponse(
            user_id=obj.get("user_id"),
            items=items,
            address=obj.get("address"),
            note=obj.get("note"),
            total_items=obj.get("total_items", 0),
            total_price=obj.get("total_price", 0.0),
            last_update=obj.get("last_update"),
            type_vat=obj.get("type_vat"),
        )

    async def _save_cart(self, cart: CartResponse) -> Dict[str, Any]:
        cart = Helper._recalc(cart)
        try:
            await self.redis.set(Helper._key(cart.user_id), cart.json(), ex=24*3600) # Auto clear after 24h
        except RedisError as e:
            raise ErrorCode.GeneralError(str(e))
        return cart.dict()

    async def add_item(self, user_id: str, data: AddCart) -> Dict[str, Any]:
        cart = await self._load_cart(user_id, required=False) or CartResponse(user_id=user_id)

        item = data.item
        idx = next((i for i, it in enumerate(cart.items) if it.product_id == item.product_id), -1)

        if idx >= 0:
            existing = cart.items[idx]
            cart.items[idx] = CartItem(
                product_id=existing.product_id,
                name=item.name or existing.name,
                price=item.price if item.price is not None else existing.price,
                quantity=int(existing.quantity) + int(item.quantity),
                image=item.image or existing.image,
            )
        else:
            cart.items.append(item)

        if data.address is not None: cart.address = data.address
        if data.note is not None: cart.note = data.note
        if data.type_vat is not None: cart.type_vat = data.type_vat

        return await self._save_cart(cart)

    async def edit(self, user_id: str, data: EditCart) -> Dict[str, Any]:
        cart = await self._load_cart(user_id, required=True)

        if data.product_id:
            idx = next((i for i, it in enumerate(cart.items) if it.product_id == data.product_id), -1)
            if idx < 0:
                raise ErrorCode.ItemNotFound()

            current = cart.items[idx]
            if data.quantity is not None and data.quantity <= 0:
                del cart.items[idx]
            else:
                cart.items[idx] = CartItem(
                    product_id=current.product_id,
                    name=data.name or current.name,
                    price=data.price if data.price is not None else current.price,
                    quantity=data.quantity if data.quantity is not None else current.quantity,
                    image=data.image or current.image,
                )

        if data.address is not None: cart.address = data.address
        if data.note is not None: cart.note = data.note
        if data.type_vat is not None: cart.type_vat = data.type_vat

        return await self._save_cart(cart)

    async def delete(self, user_id: str, data: DeleteCart) -> Dict[str, Any]:
        if data.product_id is None:
            try:
                removed = await self.redis.delete(Helper._key(user_id))
            except RedisError as e:
                raise ErrorCode.GeneralError(str(e))
            if removed == 0:
                raise ErrorCode.ItemNotFound()
            return CartResponse(user_id=user_id, items=[], last_update=Helper.get_timestamp()).dict()

        cart = await self._load_cart(user_id, required=True)
        before = len(cart.items)
        cart.items = [it for it in cart.items if it.product_id != data.product_id]
        if len(cart.items) == before:
            raise ErrorCode.ItemNotFound()
        return await self._save_cart(cart)

    async def get_cart(self, user_id: str) -> Dict[str, Any]:
        return (await self._load_cart(user_id, required=True)).dict()

    async def list_items(self, user_id: str) -> List[Dict[str, Any]]:
        return [it.dict() for it in (await self._load_cart(user_id, required=True)).items]
