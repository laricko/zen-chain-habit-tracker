from sqlalchemy.orm import Mapped

from core.db.base import Base


class User(Base):
    __tablename__ = "user"
    
    telegram_chat_id: Mapped[int]
