# AI Content Manager Telegram Bot (MVP)

MVP Telegram-бот с модульной архитектурой:
- Telegram слой (`aiogram`)
- Reasoning-агент на Claude API с tool-use
- Планировщик задач (`APScheduler`)
- Медиа-сервис (изображения/видео)
- Хранилище (SQLite через SQLAlchemy)
- Абстрактный интерфейс `Publisher` для расширения на другие соцсети

## Структура

```text
src/
  main.py
  config/settings.py
  bot/handlers.py
  agent/claude_agent.py
  tools/tool_registry.py
  services/content_service.py
  services/media_service.py
  services/publisher_service.py
  publishers/base.py
  publishers/telegram_publisher.py
  scheduler/task_scheduler.py
  db/database.py
  models/entities.py
```

## Быстрый старт

1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. Создать `.env`:
```env
TELEGRAM_BOT_TOKEN=...
CLAUDE_API_KEY=...
PUBLISH_TARGET_CHAT_ID=@your_channel_or_chat_id
DATABASE_URL=sqlite+aiosqlite:///./mvp.db
```

3. Запустить:
```bash
python -m src.main
```

## Пример сценария
1. Пользователь пишет: `сделай пост на тему ИИ в маркетинге и напомни раз в 2 дня в 10 утра`.
2. Claude выбирает tools: `create_post` + `schedule_reminder`.
3. Бот формирует черновик и отправляет preview с кнопками `Опубликовать` / `Отменить`.
4. Пользователь нажимает `Опубликовать`.
5. Бот публикует в канал/чат через Telegram Publisher и пишет в историю действий.
