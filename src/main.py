import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy import select

from src.config.settings import settings
from src.db.database import engine, Base, SessionLocal
from src.bot.handlers import router
from src.agent.claude_agent import ClaudeAgent
from src.publishers.telegram_publisher import TelegramPublisher
from src.services.content_service import ContentService
from src.services.media_service import MediaService
from src.scheduler.task_scheduler import TaskScheduler


class ServicesMiddleware(BaseMiddleware):
    def __init__(self, agent, media_service, publisher, scheduler):
        self.agent = agent
        self.media_service = media_service
        self.publisher = publisher
        self.scheduler = scheduler

    async def __call__(self, handler, event, data):
        async with SessionLocal() as session:
            data["session"] = session
            data["agent"] = self.agent
            data["media_service"] = self.media_service
            data["content_service"] = ContentService(session=session, publisher=self.publisher)
            data["scheduler"] = self.scheduler
            return await handler(event, data)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await init_db()

    bot = Bot(settings.telegram_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    agent = ClaudeAgent(settings.claude_api_key, settings.claude_model)
    media_service = MediaService()
    publisher = TelegramPublisher(bot, settings.publish_target_chat_id)
    scheduler = TaskScheduler()
    scheduler.start()

    dp.update.middleware(ServicesMiddleware(agent, media_service, publisher, scheduler))
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
