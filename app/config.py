from dataclasses import dataclass
import os


@dataclass
class Settings:
    bot_token: str
    anthropic_api_key: str
    publish_target_chat_id: str
    database_url: str = "sqlite:///./bot.db"



def load_settings() -> Settings:
    return Settings(
        bot_token=os.getenv("BOT_TOKEN", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        publish_target_chat_id=os.getenv("PUBLISH_TARGET_CHAT_ID", ""),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./bot.db"),
    )
