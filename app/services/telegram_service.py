import asyncio
from telegram import Bot
from app.config import get_settings

settings = get_settings()

from app.schemas import TelegramSchema
import logging

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.bot = Bot(token=self.token) if self.token else None

    async def send_message(self, telegram_data: TelegramSchema):
        if not self.bot or not self.chat_id:
            logger.warning("Telegram not configured")
            return

        try:
            await self.bot.send_message(chat_id=self.chat_id, text=telegram_data.message)
            logger.info(f"Telegram message sent to {self.chat_id}")
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")

    async def send_price_drop_alert(self, card_name: str, old_price: float, new_price: float):
        message = f"📉 Price Drop Alert!\nCard: {card_name}\nOld Price: ${old_price}\nNew Price: ${new_price}"
        await self.send_message(TelegramSchema(message=message))

    async def send_new_purchase_alert(self, card_name: str, price: float):
        message = f"🆕 New Purchase!\nCard: {card_name}\nPrice: ${price}"
        await self.send_message(TelegramSchema(message=message))

telegram_service = TelegramService()
