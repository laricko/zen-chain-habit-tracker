from telegram import Update
from telegram.ext import ContextTypes

from app.exceptions import EntityNotFound
from app.services.progress import get_last_progress_by_user_id
from app.services.user import get_user_by_telegram_chat_id
from telegram_bot.consts import DEFAULT_MARKUP


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user = update.effective_user

    welcome_text = (
        f"👋 Hello {telegram_user.first_name}\\!\n\n"
        "Welcome to the Habit Tracker Bot\\.\n"
        "What would you like to do today?"
    )

    await update.message.reply_text(text=welcome_text, reply_markup=DEFAULT_MARKUP, parse_mode="MarkdownV2")
