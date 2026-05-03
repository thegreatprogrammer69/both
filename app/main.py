import asyncio
from dataclasses import dataclass
import logging

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
from app.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


@dataclass
class Container:
    settings: object
    session_factory: object
    repo_cls: object
    tools_factory: object


async def main():
    setup_logging()
    load_dotenv()
    settings = load_settings()
    logger.info("Starting AI content manager bot")

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    session_factory = create_session_factory(settings)
    logger.info("Database initialized: %s", settings.database_url)

    scheduler = SchedulerService()
    scheduler.start()
    logger.info("Scheduler started")

    content_service = ContentService(bot)
    publisher = TelegramPublisher(bot, settings.publish_target_chat_id)
    logger.info("Publisher configured for chat/channel: %s", settings.publish_target_chat_id)

    def tools_factory(repo):
        return ToolRegistry(content_service, scheduler, repo, publisher)

    container = Container(settings, session_factory, Repository, tools_factory)
    dp.include_router(build_router(container))
    logger.info("Router registered. Bot is polling updates")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
