# Main Menu Buttons
from telegram import KeyboardButton, ReplyKeyboardMarkup

BTN_MY_HABITS = "📋 My Habits", "habits"
BTN_PROGRESS = "📈 My Progress", "progress"
BTN_ADD_HABIT = "➕ Add New Habit", "add"

# Habit Frequency Options
BTN_DAILY = "📅 Daily"
BTN_WEEKLY = "🗓 Weekly"
BTN_MONTHLY = "🗓 Monthly"


keyboard = [
    [KeyboardButton(text=BTN_MY_HABITS[0])],
    [KeyboardButton(text=BTN_PROGRESS[0])],
    [KeyboardButton(text=BTN_ADD_HABIT[0])],
]
DEFAULT_MARKUP = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
