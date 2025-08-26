from fastapi import APIRouter
from .controllers import HomeController

router = APIRouter(prefix="/v1/home", tags=["home"])
home_controller = HomeController()


@router.get("/ping", status_code=200, 
            responses={200: {"description": "Get items success"}})
async def home():
    result = {"ping":"pong"}
    return result


@router.get("/database/export", status_code=200, responses={
                200: {"description": "Get items success"}})
async def export_database():
    try:
        return await home_controller.export_db()
    except Exception as e:
        raise None