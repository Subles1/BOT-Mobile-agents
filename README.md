# BOT Mobile agents

Репозиторий микросервисов и бота.

## Ветки
- **main** – стабильная версия
- **develop** – интеграция фич
- **feature/*/** – для задач


## P2P Rates Microservice
See [p2p_rates_service](p2p_rates_service/README.md) for usage details.

## Telegram Bot
See [bot](bot/README.md) for usage details.

## Quick start

Install dependencies for both the service and the bot:

```bash
pip install -r p2p_rates_service/requirements.txt
pip install -r bot/requirements.txt
```

Set required environment variables and run the applications.
Only the Telegram bot needs a token. You can provide it in one of two ways:

1. Export the variable in your shell:

   ```bash
   export TELEGRAM_BOT_TOKEN=<your bot token>
   ```

2. Create a `.env` file containing `TELEGRAM_BOT_TOKEN=<your bot token>` and load it (e.g., with `source .env` or using `python-dotenv`).

Then run the services:

```bash
# run the microservice
uvicorn p2p_rates_service.main:app --reload

# in another terminal run the bot
python -m bot
```
