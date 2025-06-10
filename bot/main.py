from telegram.ext import ApplicationBuilder, CommandHandler

from .handlers import commission, log, leaderboard, faq, rates
from .config import BotConfig


def main() -> None:
    config = BotConfig.from_env()
    app = ApplicationBuilder().token(config.token).build()

    app.add_handler(CommandHandler('commission', commission))
    app.add_handler(CommandHandler('log', log))
    app.add_handler(CommandHandler('leaderboard', leaderboard))
    app.add_handler(CommandHandler('faq', faq))
    app.add_handler(CommandHandler('rates', rates))

    app.run_polling()


if __name__ == '__main__':
    main()
