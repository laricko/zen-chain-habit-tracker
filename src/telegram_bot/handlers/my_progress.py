from datetime import date, timedelta

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.schemas.progress import ListOfProgressesOutDTO
from app.services.habit import get_habit_by_title_and_user_id
from app.services.progress import (
    get_last_progress_by_user_id,
    get_progresses_by_habit_id,
)
from app.services.user import get_user_by_telegram_chat_id
from telegram_bot.consts import BTN_PROGRESS, DEFAULT_MARKUP

SELECT_HABIT, EDIT_TODAY = range(2)


async def select_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    telegram_user = update.effective_user
    user = get_user_by_telegram_chat_id(telegram_chat_id=telegram_user.id)

    progresses_dto = get_last_progress_by_user_id(user_id=user.id)
    list_progresses = progresses_dto.progresses
    context.user_data["user"] = user

    if progresses_dto.progresses:
        text = "📝 *Your Last Habit Progresses Overview:*\n\n" + "\n".join(
            f"\\- *{p.habit.title.capitalize()}* \\({p.habit.frequency}\\): {p.current}/{p.goal} \\- {p.created_date.strftime('%d\\.%m')}"
            for p in list_progresses
        )
        text += "\n\n*Choose a habit to get detailed data\\.*"
        
        habit_titles = [[habit_title] for habit_title in progresses_dto.habit_titles]
        reply_markup = ReplyKeyboardMarkup(habit_titles, resize_keyboard=True)
    else:
        text = "_You have no progress records yet\\._"
        reply_markup = DEFAULT_MARKUP

    await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return SELECT_HABIT


async def show_habit_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_title = update.message.text.strip()
    user = context.user_data.get("user")

    habit = get_habit_by_title_and_user_id(user_id=user.id, title=selected_title)
    context.user_data["habit"] = habit

    progresses_dto: ListOfProgressesOutDTO = get_progresses_by_habit_id(habit_id=habit.id)
    today = progresses_dto.progresses[0]

    text = f"📊 *{habit.title.capitalize()}* \\({habit.frequency}\\)\n"
    text += "\n".join(
        f"*{p.created_date.strftime('%d\\.%m')}* \\- {p.current}/{p.goal}"
        for p in progresses_dto.progresses
    )
    text += (
        f"\n\n\\- Total Records: *{progresses_dto.total_count}*\n"
        f"\\- Total Progress: *{progresses_dto.total_of_currents}*\n"
        f"\\- Today's Progress: *{today.current} / {today.goal}*\n\n"
        f"_What would you like to do?_"
    )

    reply_markup = ReplyKeyboardMarkup([["Edit Today"], ["Back"]], resize_keyboard=True)

    await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
    return EDIT_TODAY


async def edit_today_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    habit = context.user_data.get("habit")
    user = context.user_data.get("user")

    if not habit or not user:
        await update.message.reply_text("Something went wrong. Please try again.", reply_markup=DEFAULT_MARKUP)
        return ConversationHandler.END

    today = date.today()

    text = (
        f"✅ Updated *{habit.title.capitalize()}*\n"
        f"Progress Today: *3 / {habit.goal}*\n\n"
        f"_Keep it going!_"
    )

    await update.message.reply_text(text=text, parse_mode="MarkdownV2", reply_markup=DEFAULT_MARKUP)
    return ConversationHandler.END


habit_update_conv = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex(f"^{BTN_PROGRESS[0]}$"), select_habit),
        CommandHandler(BTN_PROGRESS[1], select_habit),
    ],
    states={
        SELECT_HABIT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, show_habit_details)
        ],
        EDIT_TODAY: [
            MessageHandler(filters.Regex("^Edit Today$"), edit_today_handler),
            MessageHandler(filters.Regex("^Back$"), select_habit)
        ],
    },
    fallbacks=[],
)
