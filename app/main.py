import asyncio
from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.bot.handlers import build_router
from app.config import load_settings
from app.db.repositories import Repository
from app.db.session import create_session_factory
from app.publishers.telegram_publisher import TelegramPublisher
from app.scheduler.scheduler_service import SchedulerService
from app.services.content_service import ContentService
from app.agent.tools import ToolRegistry


@dataclass
class Container:
    settings: object
    session_factory: object
    repo_cls: object
    tools_factory: object


async def main():
    load_dotenv()
    settings = load_settings()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    session_factory = create_session_factory(settings)
    scheduler = SchedulerService()
    scheduler.start()

    content_service = ContentService(bot)
    publisher = TelegramPublisher(bot, settings.publish_target_chat_id)

    def tools_factory(repo):
        return ToolRegistry(content_service, scheduler, repo, publisher)

    container = Container(settings, session_factory, Repository, tools_factory)
    dp.include_router(build_router(container))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
