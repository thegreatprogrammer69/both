import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.entities import Post, ScheduledTask, ActionLog
from src.publishers.base import Publisher


class ContentService:
    def __init__(self, session: AsyncSession, publisher: Publisher):
        self.session = session
        self.publisher = publisher

    async def create_post(self, user_id: int, text: str, media_path: str | None = None) -> Post:
        post = Post(user_id=user_id, text=text, media_path=media_path, status="draft")
        self.session.add(post)
        await self.session.commit()
        await self.log(user_id, "create_post", text)
        return post

    async def publish_post(self, post_id: int) -> str:
        post = await self.session.get(Post, post_id)
        pub_id = await self.publisher.publish(post.text, post.media_path)
        post.status = "published"
        await self.session.commit()
        await self.log(post.user_id, "publish_post", f"post_id={post_id}, external_id={pub_id}")
        return pub_id

    async def schedule_reminder(self, user_id: int, cron_expr: str, payload: dict) -> ScheduledTask:
        task = ScheduledTask(user_id=user_id, task_type="reminder", cron_expr=cron_expr, payload=json.dumps(payload))
        self.session.add(task)
        await self.session.commit()
        await self.log(user_id, "schedule_reminder", cron_expr)
        return task

    async def update_schedule(self, task_id: int, new_cron_expr: str) -> ScheduledTask | None:
        task = await self.session.get(ScheduledTask, task_id)
        if not task:
            return None
        task.cron_expr = new_cron_expr
        await self.session.commit()
        await self.log(task.user_id, "update_schedule", f"task={task_id}:{new_cron_expr}")
        return task

    async def log(self, user_id: int, action: str, details: str):
        self.session.add(ActionLog(user_id=user_id, action=action, details=details))
        await self.session.commit()
