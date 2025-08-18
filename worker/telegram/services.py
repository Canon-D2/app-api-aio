from telebot.async_telebot import AsyncTeleBot
from .config import BOT_TOKEN, CHANNEL_ID, ENVIRONMENT

class BaseBot:
    def __init__(self, channel_id: str):
        self.bot = AsyncTeleBot(BOT_TOKEN)
        self.environment = ENVIRONMENT
        self.channel_id = channel_id
        self.text_mode = "HTML"

    async def send_message(self, message: str):
        # Only send when Environment is Dev
        if self.environment not in ["development"]:
            return

        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=self.text_mode,
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"Error when sending telegram message: {e}")


class SentryBot(BaseBot):
    async def send_error(self, result: dict):
        title = result.get("title")
        url = result.get("url")
        method = result.get("method")
        filename = result.get("filename")
        function_name = result.get("function")
        lineno = result.get("lineno")
        context_line = result.get("context_line")
        issues_link = result.get("issues_link")

        message = (
            f"<b>❌ SENTRY ERROR</b>\n\n"
            f"<b>Environment:</b> {self.environment}\n"
            f"<b>Title:</b> {title}\n"
            f"<b>URL:</b> {url}\n"
            f"<b>Method:</b> {method}\n"
            f"<b>Filename:</b> {filename}\n"
            f"<b>Function:</b> {function_name}\n"
            f"<b>Lineno:</b> {lineno}\n"
            f"<b>Context:</b><pre>{context_line}</pre>\n"
            f"<b>Issue link:</b> {issues_link}"
        )
        await self.send_message(message)


sentry_bot = SentryBot(CHANNEL_ID)
