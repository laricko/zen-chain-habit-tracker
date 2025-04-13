import logging

from core.utils.db import validate_database

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(module)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting application...")
    logger.info("Validating a database...")
    validate_database()
