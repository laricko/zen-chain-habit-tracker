from datetime import date, datetime
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Progress(Base):
    __tablename__ = "progress"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    habit_id: Mapped[UUID] = mapped_column(ForeignKey("habit.id", ondelete="CASCADE"))
    current: Mapped[int]
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
    created_date: Mapped[date] = mapped_column(server_default=func.now())
    goal: Mapped[int]

    __table_args__ = (
        UniqueConstraint("habit_id", "created_date", name="uq_user_created_date"),
    )
