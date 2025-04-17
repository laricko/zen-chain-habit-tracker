from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.config import config
from app.exceptions import EntityNotFound
from app.services.progress import get_last_progress_by_user_id
from app.services.user import get_by_telegram_chat_id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user = update.effective_user

    welcome_text = (
        f"👋 Hello {telegram_user.first_name}\\!\n\n"
        "Welcome to the Habit Tracker Bot\\.\n"
        "What would you like to do today?"
    )

    try:
        user = get_by_telegram_chat_id(telegram_chat_id=telegram_user.id)
    except EntityNotFound:
        user = None

    if user:
        progresses = get_last_progress_by_user_id(user_id=user.id)

        table = "\n📝 **Your Habit Progresses:**\n\n" + "\n".join(
            f"\\- *{p.habit.title.capitalize()}* \\({p.habit.frequency}\\): {p.current}/{p.goal} \\- {p.created_date.strftime('%d\\.%m')}"
            for p in progresses.progresses
        )

        welcome_text += (
            "\n"
            f"{table}"
        )

    keyboard = [
        [KeyboardButton(text="📋 My Habits")],
        [KeyboardButton(text="➕ Add New Habit")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode="MarkdownV2")


def create_app():
    telegram_bot_token = config.telegram_bot_token
    app = ApplicationBuilder().token(telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
