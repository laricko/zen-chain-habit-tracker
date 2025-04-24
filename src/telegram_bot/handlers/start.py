from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.exceptions import EntityNotFound, UniqueConstraintViolation
from app.schemas.user import CreateUserDTO
from app.services.user import create_user, get_user_by_telegram_chat_id
from telegram_bot.consts import DEFAULT_MARKUP

timezones = [
    ["UTC-12, Etc/GMT+12"],
    ["UTC-11, Pacific/Pago_Pago"],
    ["UTC-10, Pacific/Honolulu"],
    ["UTC-9, America/Anchorage"],
    ["UTC-8, America/Los_Angeles"],
    ["UTC-7, America/Denver"],
    ["UTC-6, America/Chicago"],
    ["UTC-5, America/New_York"],
    ["UTC-4, America/Halifax"],
    ["UTC-3, America/Argentina/Buenos_Aires"],
    ["UTC-2, America/Noronha"],
    ["UTC-1, Atlantic/Azores"],
    ["UTC+0, Etc/UTC"],
    ["UTC+1, Europe/Berlin"],
    ["UTC+2, Europe/Istanbul"],
    ["UTC+3, Europe/Moscow"],
    ["UTC+4, Asia/Dubai"],
    ["UTC+5, Asia/Karachi"],
    ["UTC+6, Asia/Dhaka"],
    ["UTC+7, Asia/Bangkok"],
    ["UTC+8, Asia/Shanghai"],
    ["UTC+9, Asia/Tokyo"],
    ["UTC+10, Australia/Sydney"],
    ["UTC+11, Pacific/Noumea"],
    ["UTC+12, Pacific/Auckland"]
]

set_of_timezones = {
    "UTC-12, Etc/GMT+12", "UTC-11, Pacific/Pago_Pago", "UTC-10, Pacific/Honolulu",
    "UTC-9, America/Anchorage", "UTC-8, America/Los_Angeles", "UTC-7, America/Denver",
    "UTC-6, America/Chicago", "UTC-5, America/New_York", "UTC-4, America/Halifax",
    "UTC-3, America/Argentina/Buenos_Aires", "UTC-2, America/Noronha",
    "UTC-1, Atlantic/Azores", "UTC+0, Etc/UTC", "UTC+1, Europe/Berlin",
    "UTC+2, Europe/Istanbul", "UTC+3, Europe/Moscow", "UTC+4, Asia/Dubai",
    "UTC+5, Asia/Karachi", "UTC+6, Asia/Dhaka", "UTC+7, Asia/Bangkok",
    "UTC+8, Asia/Shanghai", "UTC+9, Asia/Tokyo", "UTC+10, Australia/Sydney",
    "UTC+11, Pacific/Noumea", "UTC+12, Pacific/Auckland"
}


timezone_keyboard = ReplyKeyboardMarkup(
    timezones, resize_keyboard=True, one_time_keyboard=True
)

ASK_TIMEZONE = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    telegram_user = update.effective_user
    try:
        user = get_user_by_telegram_chat_id(telegram_chat_id=telegram_user.id)
    except EntityNotFound:
        user = None

    if not user:
        await update.message.reply_text(
            f"👋 Hello {telegram_user.first_name}!\n\n"
            "Please select your timezone:",
            reply_markup=timezone_keyboard
        )
        return ASK_TIMEZONE
    await update.message.reply_text(
        f"👋 Hello {telegram_user.first_name}\\!",
        parse_mode="MarkdownV2",
        reply_markup=DEFAULT_MARKUP
    )
    return ConversationHandler.END


async def receive_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    timezone_info = update.message.text.strip()

    if timezone_info not in set_of_timezones:
        await update.message.reply_text(
            f"Please choose timezone from buttons below.",
            parse_mode="MarkdownV2",
            reply_markup=timezone_keyboard
        )
        return ASK_TIMEZONE

    _, timezone = timezone_info.split(",")
    timezone = timezone.lstrip()
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
