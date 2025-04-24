from telegram import Update
from telegram.ext import ContextTypes

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "❓ Sorry, I didn't understand that. Please use the menu or type a valid command."
    )
