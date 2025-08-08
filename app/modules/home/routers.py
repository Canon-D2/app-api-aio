from fastapi import APIRouter

router = APIRouter(prefix="/v1/home", tags=["home"])

@router.get("")
async def home():
    return {"ping":"pong"}