from telegram import Update
from telegram.ext import ContextTypes

from .config import BotConfig

config = BotConfig.from_env()

async def commission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(config.commission_text)

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(config.log_text)

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(config.leaderboard_text)

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(config.faq_text)

async def rates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(config.rates_text)
