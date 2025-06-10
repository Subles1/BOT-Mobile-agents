# Telegram Bot

A simple Telegram bot for mobile agents.

## Running

Install dependencies:
```bash
pip install -r requirements.txt
```

Set the `TELEGRAM_BOT_TOKEN` environment variable before running the bot. You can:

1. Export it in your shell:

   ```bash
   export TELEGRAM_BOT_TOKEN=<your bot token>
   ```

2. Create a `.env` file containing `TELEGRAM_BOT_TOKEN=<your bot token>` and load it (e.g., with `source .env` or using `python-dotenv`).

Then start the bot:
```bash
python -m bot
```

The bot supports the following commands:
- `/commission` – upload an XLSX report to calculate commissions
- `/leaderboard`
- `/faq` – ask a question about the service
- `/rates`
