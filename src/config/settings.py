from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    claude_api_key: str = os.getenv("CLAUDE_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./mvp.db")
    publish_target_chat_id: str = os.getenv("PUBLISH_TARGET_CHAT_ID", "")
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-latest")


settings = Settings()
