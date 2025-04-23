from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Habit(Base):
    __tablename__ = "habit"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    goal: Mapped[int]
    frequency: Mapped[str] = mapped_column(String(7))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "title", name="uq_user_title"),
        CheckConstraint(
            "frequency IN ('daily', 'weekly', 'monthly')",
            name="check_frequency_valid"
        ),
    )
