import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.agent.claude_agent import ClaudeAgent
from app.bot.keyboards import preview_keyboard

logger = logging.getLogger(__name__)


def build_router(container):
    router = Router()

    @router.message(F.text)
    async def on_text(message: Message):
        logger.info("Received text command from user=%s: %s", message.from_user.id, message.text)
        session = container.session_factory()
        repo = container.repo_cls(session)
        user = repo.get_or_create_user(message.from_user.id)
        tools = container.tools_factory(repo)
        agent = ClaudeAgent(container.settings.anthropic_api_key, tools, user.id)
        outcome = await agent.run(message.text)

        draft_id = None
        text = "Готово"
        for item in outcome["tools_called"]:
            if item["tool"] == "create_post":
                draft_id = item["result"]["draft_id"]
                text = item["result"]["text"]

        if draft_id:
            logger.info("Sending preview for draft_id=%s to user=%s", draft_id, message.from_user.id)
            await message.answer(f"Предпросмотр:\n\n{text}", reply_markup=preview_keyboard(draft_id))
        else:
            logger.info("No draft created for user=%s, returning tool output", message.from_user.id)
            await message.answer(f"Выполнено: {outcome['raw']}")

    @router.message(F.photo)
    async def on_photo(message: Message):
        logger.info("Received photo from user=%s", message.from_user.id)
        await message.answer("Фото получено. Отправь команду, например: 'убери людей с фона и добавь текст'.")

    @router.message(F.video)
    async def on_video(message: Message):
        logger.info("Received video from user=%s", message.from_user.id)
        await message.answer("Видео получено. Отправь команду, например: 'добавь субтитры'.")

    @router.callback_query(F.data.startswith("publish:"))
    async def on_publish(callback: CallbackQuery):
        draft_id = int(callback.data.split(":")[1])
        logger.info("Publish confirmed for draft_id=%s by user=%s", draft_id, callback.from_user.id)
        session = container.session_factory()
        repo = container.repo_cls(session)
        tools = container.tools_factory(repo)
        result = await tools.publish_post(draft_id)
        logger.info("Draft published: draft_id=%s message_id=%s", draft_id, result["message_id"])
        await callback.message.edit_text(f"✅ Опубликовано. message_id={result['message_id']}")

    @router.callback_query(F.data.startswith("cancel:"))
    async def on_cancel(callback: CallbackQuery):
        draft_id = int(callback.data.split(":")[1])
        logger.info("Publish canceled for draft_id=%s by user=%s", draft_id, callback.from_user.id)
        session = container.session_factory()
        repo = container.repo_cls(session)
        repo.update_draft_status(draft_id, "cancelled")
        await callback.message.edit_text("❌ Публикация отменена")

    return router
