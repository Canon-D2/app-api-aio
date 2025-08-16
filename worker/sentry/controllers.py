from .schemas import Response
from .services import SentryServices


class SentryController:
    def __init__(self) -> None:
        self.service = SentryServices()
        
    async def capture_issues(self, data: dict) -> Response:
        result = await self.service.parse(data)
        # await sentry_bot.send_error(result) # Telegram bot
        return result
