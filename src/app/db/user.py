from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.db.base import Base


class User(Base):
    __tablename__ = "user"

    telegram_chat_id: Mapped[int] = mapped_column(unique=True)
    timezone: Mapped[str] = mapped_column(String(31), nullable=True)
