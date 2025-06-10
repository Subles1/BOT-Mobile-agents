import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


def get_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN env var is required")
    return token


async def commission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /commission command."""
    await update.message.reply_text("Our commission is 5% of each deal.")


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /leaderboard command."""
    await update.message.reply_text("Leaderboard functionality coming soon.")


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /faq command."""
    await update.message.reply_text("Visit example.com/faq for answers to common questions.")


async def rates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /rates command."""
    await update.message.reply_text("Check current rates at example.com/rates.")


def main() -> None:
    """Run the Telegram bot."""
    token = get_token()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("commission", commission))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("rates", rates))
    app.run_polling()


if __name__ == "__main__":
    main()
