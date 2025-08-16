from fastapi import APIRouter

router = APIRouter(prefix="/v1/home", tags=["home"])

@router.get("", status_code=200, 
            responses={200: {"description": "Get items success"}})
async def home():
    result = {"ping":"pong"}
    return result