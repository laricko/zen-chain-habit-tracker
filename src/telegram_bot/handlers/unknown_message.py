from telegram import Update
from telegram.ext import ContextTypes

from telegram_bot.consts import DEFAULT_MARKUP


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "❓ Sorry, I didn't understand that. Please use the menu or type a valid command.",
        reply_markup=DEFAULT_MARKUP
    )
