from aiogram import Bot

from app.publishers.base import Publisher


class TelegramPublisher(Publisher):
    def __init__(self, bot: Bot, target_chat_id: str):
        self.bot = bot
        self.target_chat_id = target_chat_id

    async def publish(self, text: str, image_path: str | None = None, video_path: str | None = None) -> str:
        if video_path:
            with open(video_path, "rb") as file:
                msg = await self.bot.send_video(self.target_chat_id, file, caption=text)
        elif image_path:
            with open(image_path, "rb") as file:
                msg = await self.bot.send_photo(self.target_chat_id, file, caption=text)
        else:
            msg = await self.bot.send_message(self.target_chat_id, text)
        return str(msg.message_id)
