from telegram import Update
from telegram.ext import ContextTypes

from app.exceptions import UniqueConstraintViolation
from app.schemas.user import CreateUserDTO
from app.services.user import create_user
from telegram_bot.consts import DEFAULT_MARKUP


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user = update.effective_user

    welcome_text = (
        f"👋 Hello {telegram_user.first_name}\\!\n\n"
        "Welcome to the Habit Tracker Bot\\.\n"
        "What would you like to do today?"
    )

    try:
        create_user(CreateUserDTO(telegram_chat_id=telegram_user.id))
    except UniqueConstraintViolation:
        pass

    await update.message.reply_text(text=welcome_text, reply_markup=DEFAULT_MARKUP, parse_mode="MarkdownV2")
