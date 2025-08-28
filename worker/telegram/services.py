from telebot.async_telebot import AsyncTeleBot
from .config import BOT_TOKEN, CHANNEL_ID, ENVIRONMENT
from app.utils.helper import Helper

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
    async def send_telegram(self, result: dict):
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


class InvoiceBot(BaseBot):
    async def send_telegram(self, invoice: dict):
        items_text = ""
        for idx, item in enumerate(invoice.get("items", []), start=1):
            items_text += (
                f"\n  {idx}. <b>{item.get('name')}</b>\n"
                f"     ID: {item.get('product_id')}\n"
                f"     Qty: {item.get('quantity')} | "
                f"Price: {item.get('price')} | "
                f"Total: {float(item.get('price', 0)) * int(item.get('quantity', 0))}"
            )

        message = (
            f"<b>🧾 NEW INVOICE</b>\n"
            f"<b>Invoice ID:</b> {invoice.get('_id', '-')}\n"
            f"<b>User ID:</b> {invoice.get('user_id')}\n"
            f"<b>Status:</b> {invoice.get('status', '-')}\n"
            f"<b>Type VAT:</b> {invoice.get('type_vat', '-')}\n"
            f"<b>Created At:</b> {Helper.timestamp_to_date(invoice.get('created_at'))}\n\n"
            f"<b>Items:</b>{items_text}\n\n"
            f"<b>Total Items:</b> {invoice.get('total_items', 0)}\n"
            f"<b>Total Price:</b> {invoice.get('total_price', 0.0)}\n"
            f"<b>Address:</b> {invoice.get('address', '-')}\n"
            f"<b>Note:</b> {invoice.get('note', '-')}"
        )

        await self.send_message(message)




sentry_bot = SentryBot(CHANNEL_ID)
invoice_bot = InvoiceBot(CHANNEL_ID)