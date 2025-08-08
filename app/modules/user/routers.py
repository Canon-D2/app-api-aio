from fastapi import APIRouter, Query, Path
from . import schemas
from .controllers import UserController
from typing import Optional
from .exception import ErrorCode

router = APIRouter(prefix="/v1/users", tags=["users"])
controller = UserController()


@router.post("", response_model=str)
async def create_user(data: schemas.UserCreate):
    return await controller.create(data.model_dump())


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: str = Path(...)):
    user = await controller.get_by_id(user_id)
    if not user:
        raise ErrorCode.InvalidUserId()
    return user


@router.put("/{user_id}", response_model=bool)
async def update_user(user_id: str, data: schemas.UserUpdate):
    return await controller.update(user_id, data.model_dump(exclude_unset=True))


@router.delete("/{user_id}", response_model=bool)
async def delete_user(user_id: str):
    return await controller.delete(user_id)


@router.get("", response_model=schemas.PaginatedUserResponse)
async def list_users(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    search: Optional[str] = None,
):
    query = {}
    if search:
        query["$or"] = [
            {"email": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
        ]
    return await controller.search(query, page, limit)
