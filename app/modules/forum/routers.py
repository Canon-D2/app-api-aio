from typing import Optional
from fastapi import APIRouter, Query, Path
from . import schemas
from .controllers import ThreadController, PostController
from .exception import ErrorCode

router = APIRouter(prefix="/v1/forum", tags=["forum"])

thread_controller = ThreadController()
post_controller = PostController()


@router.post("/threads/create", status_code=201, responses={
                201: {"model": schemas.ThreadResponse, "description": "Create items success"}})
async def create_thread(data: schemas.ThreadCreate):
    result = await thread_controller.create(data.model_dump())
    return result


@router.get("/threads/get/{thread_id}", status_code=200, responses={
                200: {"model": schemas.ThreadResponse, "description": "Get items success"}})
async def get_thread(thread_id: str = Path(...)):
    result = await thread_controller.get(thread_id)
    if not result:
        raise ErrorCode.ThreadNotFound()
    return result


@router.put("/threads/edit/{thread_id}", status_code=200, responses={
                200: {"model": schemas.ThreadResponse, "description": "Edit items success"}})
async def update_thread(thread_id: str, data: schemas.ThreadUpdate):
    result = await thread_controller.update(thread_id, data.model_dump(exclude_unset=True))
    return result


@router.delete("/threads/delete/{thread_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_thread(thread_id: str):
    result = await thread_controller.delete(thread_id)
    return result


@router.get("/threads/search", status_code=200, responses={
                200: {"model": schemas.PaginatedThreadResponse, "description": "Get items success"}})
async def list_threads(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    theme: Optional[str] = None,
    title: Optional[str] = None
):
    query = {}
    if theme: query["theme"] = {"$regex": theme, "$options": "i"}
    if title: query["title"] = {"$regex": title, "$options": "i"}

    result = await thread_controller.search(query, page, limit)
    return result


@router.post("/posts/create", status_code=201, responses={
                201: {"model": schemas.PostResponse, "description": "Create items success"}})
async def create_post(data: schemas.PostCreate):
    result = await post_controller.create(data.model_dump())
    return result

@router.get("/posts/get/{post_id}", status_code=200, responses={
                200: {"model": schemas.PostResponse, "description": "Get items success"}})
async def get_post(post_id: str = Path(...)):
    result = await post_controller.get(post_id)
    if not result:
        raise ErrorCode.PostNotFound()
    return result

@router.put("/posts/edit/{post_id}", status_code=200, responses={
                200: {"model": schemas.PostResponse, "description": "Edit items success"}})
async def update_post(post_id: str, data: schemas.PostUpdate):
    result = await post_controller.update(post_id, data.model_dump(exclude_unset=True))
    return result


@router.delete("/posts/delete/{post_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_post(post_id: str):
    result = await post_controller.delete(post_id)
    return result


@router.get("/posts/search", status_code=200, responses={
                200: {"model": schemas.PaginatedPostResponse, "description": "Get items success"}})
async def list_posts(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    thread_id: Optional[str] = None,
    author_id: Optional[str] = None
):
    query = {}
    if thread_id: query["thread_id"] = thread_id
    if author_id: query["author.user_id"] = author_id

    result = await post_controller.search(query, page, limit)
    return result


@router.post("/posts/reactions/{post_id}", status_code=200, responses={
                200: {"description": "Create/Edit/Delete items success"}})
async def reaction(post_id: str, reaction: str = Query(...), user_id: str = Query(...)):
    resullt = await post_controller.reaction(post_id, reaction, user_id)
    return resullt