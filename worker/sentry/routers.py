from fastapi import APIRouter
from .controllers import SentryController
from . import schemas


router = APIRouter(prefix="/v1/sentry", tags=["sentry"])
sentry_controller = SentryController()


@router.post("/issues", status_code=201, responses={
                201: {"model": schemas.Response, "description": "Post items success"}})
async def capture_issues(data: dict):
    result = await sentry_controller.capture_issues(data)
    print("[SENTRY-WEBHOOK]", result)
    return schemas.Response(**result)


@router.get("/bug", status_code=500, responses={
                500: {"description": "Test sentry success"}})
async def test_bug():
    test = 1 / 0
    return test
