from sqlalchemy import select

from app.models.entities import ActionLog, ContentDraft, ScheduledTask, User


class Repository:
    def __init__(self, session):
        self.session = session

    def get_or_create_user(self, telegram_user_id: int) -> User:
        user = self.session.scalar(select(User).where(User.telegram_user_id == telegram_user_id))
        if user:
            return user
        user = User(telegram_user_id=telegram_user_id)
        self.session.add(user)
        self.session.commit()
        return user

    def create_draft(self, user_id: int, text: str = "", image_path: str | None = None, video_path: str | None = None) -> ContentDraft:
        draft = ContentDraft(user_id=user_id, text=text, image_path=image_path, video_path=video_path)
        self.session.add(draft)
        self.session.commit()
        return draft

    def get_draft(self, draft_id: int) -> ContentDraft | None:
        return self.session.get(ContentDraft, draft_id)

    def update_draft_status(self, draft_id: int, status: str) -> None:
        draft = self.session.get(ContentDraft, draft_id)
        if draft:
            draft.status = status
            self.session.commit()

    def create_schedule(self, user_id: int, cron_expr: str, description: str, job_id: str) -> ScheduledTask:
        task = ScheduledTask(user_id=user_id, cron_expr=cron_expr, description=description, job_id=job_id)
        self.session.add(task)
        self.session.commit()
        return task

    def delete_schedule(self, job_id: str) -> None:
        task = self.session.scalar(select(ScheduledTask).where(ScheduledTask.job_id == job_id))
        if task:
            self.session.delete(task)
            self.session.commit()

    def log_action(self, user_id: int, action_type: str, payload: str = "") -> None:
        log = ActionLog(user_id=user_id, action_type=action_type, payload=payload)
        self.session.add(log)
        self.session.commit()
