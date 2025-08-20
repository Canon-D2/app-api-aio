from .services import AppSheetService


class AppSheetController:
    def __init__(self):
        self.appsheet_service = AppSheetService()

    async def send_report(self, data: dict):
        result = await self.appsheet_service.send_report(data)
        return result

    async def get_report(self, page: int, limit: int):
        result =  await self.appsheet_service.get_report(page, limit)
        return result