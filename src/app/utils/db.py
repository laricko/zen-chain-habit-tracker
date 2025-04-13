import logging

from sqlalchemy import create_engine, text

from app.config import config
from app.db.base import Base

logger = logging.getLogger()
engine = create_engine(config.pg_dsn)


def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection is healthy!")
    except Exception as e:
        logger.exception(f"Database connection failed: {e}")


def validate_database():
    Base.metadata.create_all(engine)

    check_db_connection()
