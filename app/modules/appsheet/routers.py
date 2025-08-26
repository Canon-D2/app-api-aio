from fastapi import APIRouter
from .schemas import ReportRequest
from .controllers import AppSheetController


router = APIRouter(prefix="/v1/appsheet", tags=["app-sheet"])
appsheet_controller = AppSheetController()


@router.post("/send-report", status_code=200, responses={
                200: {"description": "Post items success"}})
async def send_report(data: ReportRequest):
    result =  await appsheet_controller.send_report(data.dict())
    return result

@router.get("/get-report", status_code=200,
            responses={200: {"description": "Get report success"}})
async def get_report(page: int = 1, limit: int = 10):
    return await appsheet_controller.get_report(page, limit)