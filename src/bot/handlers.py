from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.claude_agent import ClaudeAgent
from src.services.content_service import ContentService
from src.services.media_service import MediaService

router = Router()


@router.message(F.text)
async def handle_text(message: Message, session: AsyncSession, agent: ClaudeAgent, content_service: ContentService, media_service: MediaService):
    user_text = message.text
    actions = await agent.plan(user_text)

    draft_post = None
    reply_lines = ["🧠 План действий агента:"]

    for action in actions:
        tool = action["tool"]
        data = action["input"]
        reply_lines.append(f"- {tool}: {data}")

        if tool == "create_post":
            draft_post = await content_service.create_post(message.from_user.id, data.get("text", ""), data.get("media_path"))

        elif tool == "generate_images":
            paths = await media_service.generate_images(data["prompt"], data.get("count", 1))
            if draft_post and paths:
                draft_post.media_path = paths[0]
                await session.commit()

        elif tool == "schedule_reminder":
            await content_service.schedule_reminder(message.from_user.id, data["cron_expr"], data.get("payload", {}))

        elif tool == "update_schedule":
            await content_service.update_schedule(data["task_id"], data["new_cron_expr"])

    await message.answer("\n".join(reply_lines))

    if draft_post:
        kb = InlineKeyboardBuilder()
        kb.button(text="Опубликовать", callback_data=f"publish:{draft_post.id}")
        kb.button(text="Отменить", callback_data=f"cancel:{draft_post.id}")
        kb.adjust(2)
        preview = f"👀 Предпросмотр поста:\n\n{draft_post.text}"
        await message.answer(preview, reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("publish:"))
async def publish_callback(callback: CallbackQuery, content_service: ContentService):
    post_id = int(callback.data.split(":", 1)[1])
    await content_service.publish_post(post_id)
    await callback.message.answer("✅ Пост опубликован.")
    await callback.answer()


@router.callback_query(F.data.startswith("cancel:"))
async def cancel_callback(callback: CallbackQuery, session: AsyncSession):
    from src.models.entities import Post

    post_id = int(callback.data.split(":", 1)[1])
    post = await session.get(Post, post_id)
    if post:
        post.status = "cancelled"
        await session.commit()
    await callback.message.answer("❌ Публикация отменена.")
    await callback.answer()
