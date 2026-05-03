import uuid
from pathlib import Path

from app.services.media_service import MediaService


class ToolRegistry:
    def __init__(self, content_service, scheduler_service, repository, publisher):
        self.content_service = content_service
        self.scheduler_service = scheduler_service
        self.repository = repository
        self.publisher = publisher
        self.media_service = MediaService()

    async def create_post(self, user_id: int, topic: str) -> dict:
        text = self.content_service.generate_post_text(topic)
        draft = self.repository.create_draft(user_id=user_id, text=text)
        return {"draft_id": draft.id, "text": text}

    async def edit_image(self, input_path: str, overlay_text: str = "") -> dict:
        output = str(Path("media") / f"edited_{uuid.uuid4().hex}.jpg")
        Path("media").mkdir(exist_ok=True)
        path = self.media_service.edit_image(input_path, output, overlay_text)
        return {"image_path": path}

    async def generate_images(self, prompt: str, count: int = 1) -> dict:
        # Заглушка под Stable Diffusion/API
        generated = [f"media/generated_{i}_{prompt[:10]}.png" for i in range(count)]
        return {"images": generated}

    async def add_subtitles_to_video(self, input_path: str, subtitle_text: str) -> dict:
        output = str(Path("media") / f"sub_{uuid.uuid4().hex}.mp4")
        Path("media").mkdir(exist_ok=True)
        path = self.media_service.add_subtitles_to_video(input_path, output, subtitle_text)
        return {"video_path": path}

    async def schedule_reminder(self, user_id: int, cron_expr: str, description: str) -> dict:
        job_id = f"job_{uuid.uuid4().hex}"
        self.scheduler_service.add_cron_job(job_id, self.content_service.send_reminder, cron_expr, user_id=user_id, description=description)
        task = self.repository.create_schedule(user_id, cron_expr, description, job_id)
        return {"job_id": task.job_id}

    async def publish_post(self, draft_id: int) -> dict:
        draft = self.repository.get_draft(draft_id)
        msg_id = await self.publisher.publish(draft.text, draft.image_path, draft.video_path)
        self.repository.update_draft_status(draft_id, "published")
        return {"message_id": msg_id}
