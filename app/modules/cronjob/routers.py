from fastapi import APIRouter, Query
from . import schemas
from .controllers import CronController
from typing import Optional


router = APIRouter(prefix="/v1/cronjob", tags=["cronjob"])
controller = CronController()


@router.post("/create", status_code=201, responses={
                201: {"model": schemas.CronResponse, "description": "Create items success"}})
async def create_cron(data: schemas.CronCreate):
    result = await controller.create(data.model_dump())
    return schemas.CronResponse(**result)

@router.get("/get/{cron_id}", status_code=200, responses={
                200: {"model": schemas.CronResponse, "description": "Get items success"}})
async def get_cron(cron_id: str):
    result = await controller.get(cron_id)
    return result

@router.put("/edit/{cron_id}", status_code=200, responses={
                200: {"model": schemas.CronResponse, "description": "Edit items success"}})
async def update_cron(cron_id: str, data: schemas.CronUpdate):
    result = await controller.update(cron_id, data.model_dump(exclude_unset=True))
    return schemas.CronResponse(**result)

@router.delete("/delete/{cron_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_cron(cron_id: str):
    result = await controller.delete(cron_id)
    return result


@router.get("/search", status_code=200, responses={
                200: {"model": schemas.PaginatedCronResponse, "description": "Get items success"}})
async def list_cron(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    search: Optional[str] = None,
):
    query = {}
    if search:
        query["$or"] = [
            {"task": {"$regex": search, "$options": "i"}},
            {"endpoint": {"$regex": search, "$options": "i"}},
        ]
    result = await controller.search(query, page, limit)
    return result
