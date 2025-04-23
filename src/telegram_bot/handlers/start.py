from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.exceptions import UniqueConstraintViolation
from app.schemas.user import CreateUserDTO
from app.services.user import create_user
from telegram_bot.consts import DEFAULT_MARKUP

POPULAR_TIMEZONES = [
    ["UTC", "America/New_York", "America/Los_Angeles"],
    ["Europe/London", "Europe/Berlin", "Europe/Moscow"],
    ["Asia/Tokyo", "Asia/Kolkata", "Asia/Shanghai"],
    ["Australia/Sydney", "Africa/Nairobi"]
]

timezone_keyboard = ReplyKeyboardMarkup(
    POPULAR_TIMEZONES, resize_keyboard=True, one_time_keyboard=True
)


ASK_TIMEZONE = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    telegram_user = update.effective_user

    await update.message.reply_text(
        f"👋 Hello {telegram_user.first_name}!\n\n"
        "Please select your timezone:",
        reply_markup=timezone_keyboard
    )
    return ASK_TIMEZONE


async def receive_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    timezone = update.message.text.strip()
    telegram_user = update.effective_user

    try:
        create_user(CreateUserDTO(telegram_chat_id=telegram_user.id, timezone=timezone))
    except UniqueConstraintViolation:
        pass

    await update.message.reply_text(
        f"✅ Timezone set to `{timezone}`",
        parse_mode="MarkdownV2",
        reply_markup=DEFAULT_MARKUP
    )
    return ConversationHandler.END


start_conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        ASK_TIMEZONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_timezone)],
    },
    fallbacks=[],
)
