import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import config

logger = logging.getLogger(__name__)
engine = create_engine(config.pg_dsn)
SessionLocal = sessionmaker(engine)


def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection is healthy!")
    except Exception as e:
        logger.exception(f"Database connection failed: {e}")


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def with_session(func):
    def wrapper(*args, **kwargs):
        with get_session() as session:
            return func(*args, session=session, **kwargs)
    return wrapper
