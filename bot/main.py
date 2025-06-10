import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from .commission import calculate_commissions
from .faq import find_answer


def get_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN env var is required")
    return token


async def commission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /commission command with XLSX document."""
    message = update.message
    if not message or not message.document:
        await message.reply_text("Please attach an XLSX file with the command.")
        return

    telegram_file = await message.document.get_file()
    file_bytes = await telegram_file.download_as_bytearray()

    try:
        summary = calculate_commissions(file_bytes)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        await message.reply_text(f"Failed to process file: {exc}")
        return

    await message.reply_text(summary)


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /leaderboard command."""
    await update.message.reply_text("Leaderboard functionality coming soon.")


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /faq command."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a question after the command.")
        return

    answer = find_answer(query)
    if answer:
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text("Sorry, I don't know the answer to that question.")


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
