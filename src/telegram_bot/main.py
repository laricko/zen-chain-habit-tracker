from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from app.config import config
from telegram_bot import consts, handlers


def create_app():
    telegram_bot_token = config.telegram_bot_token
    app = ApplicationBuilder().token(telegram_bot_token).build()

    app.add_handler(handlers.start_conv)

    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex(f"^{consts.BTN_MY_HABITS[0]}$"), handlers.my_habits)
    )
    app.add_handler(CommandHandler(consts.BTN_MY_HABITS[1], handlers.my_habits))

    app.add_handler(handlers.add_habit_conv)

    app.add_handler(handlers.habit_update_conv)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.unknown_message))

    app.run_polling()
