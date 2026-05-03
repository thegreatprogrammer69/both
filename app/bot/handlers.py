from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.agent.claude_agent import ClaudeAgent
from app.bot.keyboards import preview_keyboard


def build_router(container):
    router = Router()

    @router.message(F.text)
    async def on_text(message: Message):
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
            await message.answer(f"Предпросмотр:\n\n{text}", reply_markup=preview_keyboard(draft_id))
        else:
            await message.answer(f"Выполнено: {outcome['raw']}")

    @router.message(F.photo)
    async def on_photo(message: Message):
        await message.answer("Фото получено. Отправь команду, например: 'убери людей с фона и добавь текст'.")

    @router.message(F.video)
    async def on_video(message: Message):
        await message.answer("Видео получено. Отправь команду, например: 'добавь субтитры'.")

    @router.callback_query(F.data.startswith("publish:"))
    async def on_publish(callback: CallbackQuery):
        draft_id = int(callback.data.split(":")[1])
        session = container.session_factory()
        repo = container.repo_cls(session)
        tools = container.tools_factory(repo)
        result = await tools.publish_post(draft_id)
        await callback.message.edit_text(f"✅ Опубликовано. message_id={result['message_id']}")

    @router.callback_query(F.data.startswith("cancel:"))
    async def on_cancel(callback: CallbackQuery):
        draft_id = int(callback.data.split(":")[1])
        session = container.session_factory()
        repo = container.repo_cls(session)
        repo.update_draft_status(draft_id, "cancelled")
        await callback.message.edit_text("❌ Публикация отменена")

    return router
