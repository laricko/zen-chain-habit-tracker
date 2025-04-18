from telegram import Update
from telegram.ext import ContextTypes

from app.schemas.habit import ListOfHabits
from app.services.habit import get_habits_by_user_id
from app.services.user import get_user_by_telegram_chat_id
from telegram_bot.consts import DEFAULT_MARKUP


async def my_habits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user = update.effective_user

    user = get_user_by_telegram_chat_id(telegram_user.id)
    habits: ListOfHabits = get_habits_by_user_id(user_id=user.id)

    if not habits.habits:
        await update.message.reply_text("You have no habits yet. Use /add or button to create one.")
        return

    message = "📋 *Your Habits:*\n\n"
    for idx, habit in enumerate(habits.habits, start=1):
        message += f"{idx}\\. *{habit.title.capitalize()}* \\| frequency: {habit.frequency}, goal: {habit.goal}\n"

    await update.message.reply_text(
        message,
        parse_mode="MarkdownV2",
        reply_markup=DEFAULT_MARKUP
    )
