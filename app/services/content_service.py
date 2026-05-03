class ContentService:
    def __init__(self, bot=None):
        self.bot = bot

    def generate_post_text(self, topic: str) -> str:
        return f"🔥 Пост дня: {topic}\n\nКороткий AI-сгенерированный текст для публикации."

    async def send_reminder(self, user_id: int, description: str):
        if self.bot:
            await self.bot.send_message(user_id, f"⏰ Напоминание: {description}")
