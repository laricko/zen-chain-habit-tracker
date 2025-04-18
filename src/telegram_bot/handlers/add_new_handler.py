from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.schemas.habit import CreateHabitDTO, HabitFrequency
from app.services.habit import create_habit
from app.services.user import get_user_by_telegram_chat_id
from telegram_bot.consts import BTN_ADD_HABIT, DEFAULT_MARKUP

TITLE, GOAL, FREQUENCY = range(3)


async def start_add_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_markup = ReplyKeyboardMarkup([["/cancel"]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("📝 What's the title of your new habit?", reply_markup=reply_markup)
    return TITLE


async def ask_goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["title"] = update.message.text.strip()
    reply_markup = ReplyKeyboardMarkup([["/cancel"]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("🎯 What is your goal (a number)?", reply_markup=reply_markup)
    return GOAL


async def ask_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data["goal"] = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("⚠️ Please enter a valid number.")
        return GOAL

    reply_markup = ReplyKeyboardMarkup([["daily", "weekly", "monthly"], ["/cancel"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📆 How often? Choose frequency:", reply_markup=reply_markup)
    return FREQUENCY


async def save_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    frequency = update.message.text.strip()
    if frequency not in HabitFrequency.__members__:
        await update.message.reply_text("⚠️ Please choose one of: daily, weekly, or monthly.")
        return FREQUENCY

    telegram_user = update.effective_user
    user = get_user_by_telegram_chat_id(telegram_chat_id=telegram_user.id)

    habit_data = CreateHabitDTO(
        user_id=user.id,
        title=context.user_data["title"],
        goal=context.user_data["goal"],
        frequency=HabitFrequency[frequency]
    )

    create_habit(habit_data)
    await update.message.reply_text("✅ Habit added successfully!", reply_markup=DEFAULT_MARKUP)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Habit creation cancelled.", reply_markup=DEFAULT_MARKUP)
    return ConversationHandler.END


add_habit_conv = ConversationHandler(
    entry_points=[
        MessageHandler(filters.TEXT & filters.Regex(f"^{BTN_ADD_HABIT[0]}$"), start_add_habit),
        CommandHandler(BTN_ADD_HABIT[1], start_add_habit)
    ],
    states={
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_goal)],
        GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_frequency)],
        FREQUENCY: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_habit)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
    ]
)
