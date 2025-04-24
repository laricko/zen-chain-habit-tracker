from datetime import date

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.schemas.progress import IncrementProgressDTO, UpdateProgressDTO
from app.services.habit import delete_habit, get_habit_by_title_and_user_id
from app.services.progress import (
    get_last_progress_by_user_id,
    get_progresses_by_habit_id,
    increment_progress,
    update_progress,
)
from app.services.user import get_user_by_telegram_chat_id
from telegram_bot.consts import BTN_PROGRESS, DEFAULT_MARKUP

HABIT_DETAIL, EDIT_TODAY, CHOOSE_EDIT_ACTION, INCREMENT_VALUE, SET_VALUE, CONFIRM_DELETE = range(6)
EDIT_TODAY_BTN = "📝 Edit Today"
INCREMENT_BY_BTN = "➕ Increment by"
SET_NEW_VALUE_BTN = "✏️ Set a value"
BACK_BTN = "🔙 Back"
DELETE_HABIT_BTN = "🗑 Delete Habit"
CONFIRM_DELETE = "✅ Yes, delete"
CANCEL_DELETE = "❌ Cancel"


async def my_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    telegram_user = update.effective_user
    user = get_user_by_telegram_chat_id(telegram_chat_id=telegram_user.id)
    context.user_data["user"] = user

    progresses_dto = get_last_progress_by_user_id(user_id=user.id)
    if not progresses_dto.progresses:
        await update.message.reply_text(
            "_You have no progress records yet\\._",
            reply_markup=DEFAULT_MARKUP,
            parse_mode="MarkdownV2"
        )
        return ConversationHandler.END

    text = "📝 *Your Last Habit Progresses Overview:*\n\n" + "\n".join(
        f"\\- *{p.habit.title.capitalize()}* \\({p.habit.frequency}\\): {p.current}/{p.goal} \\- {p.created_date.strftime('%d\\.%m')}"
        for p in progresses_dto.progresses
    )
    text += "\n\n*Choose a habit to get detailed data\\.*"

    buttons = [[title] for title in progresses_dto.habit_titles]
    buttons += [[BACK_BTN]]
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
        parse_mode="MarkdownV2"
    )
    return HABIT_DETAIL


async def show_habit_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_title = update.message.text.strip()

    if selected_title == BACK_BTN:
        await update.message.reply_text("What would you like to do today?", reply_markup=DEFAULT_MARKUP)
        return ConversationHandler.END

    user = context.user_data["user"]
    habit = get_habit_by_title_and_user_id(user_id=user.id, title=selected_title)
    context.user_data["habit"] = habit
    progresses_dto = get_progresses_by_habit_id(habit_id=habit.id)
    current_progress = progresses_dto.progresses[0]
    context.user_data["current_progress"] = current_progress

    text = f"📊 *{habit.title.capitalize()}* \\({habit.frequency}\\)\n" + "\n".join(
        f"*{p.created_date.strftime('%d\\.%m')}* \\- {p.current}/{p.goal}"
        for p in progresses_dto.progresses
    )
    text += (
        f"\n\n\\- Total Records: *{progresses_dto.total_count}*\n"
        f"\\- Total Progress: *{progresses_dto.total_of_currents}*\n"
        f"\\- Today's Progress: *{current_progress.current} / {current_progress.goal}*\n\n"
        f"_What would you like to do?_"
    )

    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(
            [[EDIT_TODAY_BTN], [DELETE_HABIT_BTN], [BACK_BTN]],
            resize_keyboard=True
        ),
        parse_mode="MarkdownV2"
    )
    return EDIT_TODAY


async def edit_today_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    current_progress = context.user_data["current_progress"]
    today = current_progress.created_date.strftime('%d\\.%m')

    await update.message.reply_text(
        f"🛠 *Editing {context.user_data['habit'].title.capitalize()}* \\- *{today}*",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton(INCREMENT_BY_BTN)],
                [KeyboardButton(SET_NEW_VALUE_BTN)],
                [KeyboardButton(BACK_BTN)]
            ],
            resize_keyboard=True
        ),
        parse_mode="MarkdownV2"
    )
    return CHOOSE_EDIT_ACTION


async def ask_increment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("🔢 Enter how much to increment by:")
    return INCREMENT_VALUE


async def ask_set_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("✏️ Enter the new progress value:")
    return SET_VALUE


async def increment_value_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    value = update.message.text.strip()
    try:
        value = int(value)
    except ValueError:
        await update.message.reply_text("🚫 Please enter a valid positive number.")
        return INCREMENT_VALUE

    current_progress = context.user_data["current_progress"]
    new_progress = increment_progress(data=IncrementProgressDTO(id=current_progress.id, increment_by=value))
    await update.message.reply_text(f"✅ Progress incremented by {value}. Your current progress for today {new_progress.current}", reply_markup=DEFAULT_MARKUP)
    return ConversationHandler.END


async def set_value_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    value = update.message.text.strip()
    try:
        value = int(value)
    except ValueError:
        await update.message.reply_text("🚫 Please enter a valid positive number.")
        return SET_VALUE

    current_progress = context.user_data["current_progress"]
    new_progress = update_progress(id=current_progress.id, data=UpdateProgressDTO(current=value))
    await update.message.reply_text(f"✅ Progress set to {new_progress.current}.", reply_markup=DEFAULT_MARKUP)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Cancelled", reply_markup=DEFAULT_MARKUP)
    return ConversationHandler.END


async def confirm_delete_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    habit = context.user_data["habit"]
    await update.message.reply_text(
        f"⚠️ Are you sure you want to delete *{habit.title}*? This cannot be undone\\!",
        reply_markup=ReplyKeyboardMarkup([["Yes, delete"], ["Cancel"]], resize_keyboard=True),
        parse_mode="MarkdownV2"
    )
    return CONFIRM_DELETE


async def delete_habit_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    habit = context.user_data["habit"]
    delete_habit(id=habit.id)
    await update.message.reply_text(
        f"✅ Habit *{habit.title}* has been deleted\\.",
        reply_markup=DEFAULT_MARKUP,
        parse_mode="MarkdownV2"
    )
    return ConversationHandler.END


async def cancel_deletion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Deletion cancelled\\.", reply_markup=DEFAULT_MARKUP)
    return ConversationHandler.END


habit_update_conv = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex(f"^{BTN_PROGRESS[0]}$"), my_progress),
        CommandHandler(BTN_PROGRESS[1], my_progress),
    ],
    states={
        HABIT_DETAIL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, show_habit_details)
        ],
        EDIT_TODAY: [
            MessageHandler(filters.Regex(f"^{EDIT_TODAY_BTN}$"), edit_today_handler),
            MessageHandler(filters.Regex(f"^{DELETE_HABIT_BTN}$"), confirm_delete_habit),  # Handle delete button
            MessageHandler(filters.Regex(f"^{BACK_BTN}$"), my_progress)
        ],
        CHOOSE_EDIT_ACTION: [
            MessageHandler(filters.Regex(f"^{INCREMENT_BY_BTN}$"), ask_increment),
            MessageHandler(filters.Regex(f"^{SET_NEW_VALUE_BTN}$"), ask_set_value),
            MessageHandler(filters.Regex(f"^{BACK_BTN}$"), my_progress)
        ],
        INCREMENT_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, increment_value_handler)
        ],
        SET_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, set_value_handler)
        ],
        CONFIRM_DELETE: [
            MessageHandler(filters.Regex(f"^{CONFIRM_DELETE}$"), delete_habit_confirmed),
            MessageHandler(filters.Regex(f"^{CANCEL_DELETE}$"), cancel_deletion)
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel)
    ],
)
