# BOT Mobile agents

Репозиторий микросервисов и бота.

## Ветки
- **main** – стабильная версия
- **develop** – интеграция фич
- **feature/*/** – для задач

## Телеграм-бот

В каталоге `bot/` находится простой бот на базе `python-telegram-bot`. Для работы необходимы переменные окружения:

```
TELEGRAM_BOT_TOKEN   # токен бота
COMMISSION_TEXT      # текст для /commission
LOG_TEXT             # текст для /log
LEADERBOARD_TEXT     # текст для /leaderboard
FAQ_TEXT             # текст для /faq
RATES_TEXT           # текст для /rates
```

Установите зависимости и запустите бота:

```bash
pip install -r requirements.txt
python -m bot.main
```
