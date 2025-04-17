import logging

from app.utils.db import check_db_connection

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting application...")
    logger.info("Checking database's connection...")
    check_db_connection()
