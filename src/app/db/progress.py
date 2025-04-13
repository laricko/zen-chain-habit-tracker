from datetime import date, datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Progress(Base):
    __tablename__ = "progress"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    habit_id: Mapped[UUID] = mapped_column(ForeignKey("habit.id"))
    current: Mapped[int]
    updated_at: Mapped[datetime]
    created_date: Mapped[date]
