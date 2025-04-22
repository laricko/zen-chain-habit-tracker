import logging

from app.utils.db import check_db_connection
from telegram_bot.main import create_app as create_telegram_app


class ExcludeHttpxFilter(logging.Filter):
    def filter(self, record):
        return not record.name.startswith("httpx")


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO
)

for handler in logging.getLogger().handlers:
    handler.addFilter(ExcludeHttpxFilter())

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting application...")
    logger.info("Checking database's connection...")
    check_db_connection()
    logger.info("Starting telegram bot...")
    create_telegram_app()
