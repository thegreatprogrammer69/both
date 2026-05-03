# AI Content Manager Telegram Bot (MVP)

Модульный MVP Telegram-бота на Python с Claude API (tool-based агент):
- Telegram слой (aiogram)
- Агент reasoning + tool use (Claude)
- Планировщик задач (APScheduler)
- Сервис медиа (Pillow/OpenCV + ffmpeg)
- Слой данных (SQLite через SQLAlchemy)
- Preview before publish (кнопки Publish/Cancel)

## Структура проекта

```text
app/
  main.py
  config.py
  bot/
    handlers.py
    keyboards.py
  agent/
    claude_agent.py
    tools.py
  services/
    media_service.py
    content_service.py
  scheduler/
    scheduler_service.py
  publishers/
    base.py
    telegram_publisher.py
  db/
    base.py
    session.py
    repositories.py
  models/
    entities.py
```

## Быстрый старт

1. Создай `.env`:

```env
BOT_TOKEN=...
ANTHROPIC_API_KEY=...
PUBLISH_TARGET_CHAT_ID=-1001234567890
DATABASE_URL=sqlite:///./bot.db
```

2. Установи зависимости:

```bash
pip install -e .
```

3. Запусти:

```bash
python -m app.main
```

## Пример сценария

1. Пользователь: "сделай пост на тему X и напомни раз в 2 дня в 10 утра".
2. Claude анализирует intent и вызывает инструменты: `create_post` + `schedule_reminder`.
3. Бот генерирует текст/медиа, отправляет preview с кнопками.
4. Пользователь нажимает "Опубликовать".
5. `TelegramPublisher` публикует в канал/чат.
6. История и задачи сохраняются в БД.
