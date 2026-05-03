from aiogram import Bot
from aiogram.types import FSInputFile
from src.publishers.base import Publisher


class TelegramPublisher(Publisher):
    def __init__(self, bot: Bot, target_chat_id: str):
        self.bot = bot
        self.target_chat_id = target_chat_id

    async def publish(self, text: str, media_path: str | None = None) -> str:
        if media_path:
            msg = await self.bot.send_photo(self.target_chat_id, photo=FSInputFile(media_path), caption=text)
        else:
            msg = await self.bot.send_message(self.target_chat_id, text)
        return str(msg.message_id)
