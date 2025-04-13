from uuid import UUID

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import Base


class Habit(Base):
    __tablename__ = "habit"

    user_id: Mapped[UUID]
    title: Mapped[str] = mapped_column(String(255))
    goal: Mapped[int]
    frequency: Mapped[str] = mapped_column(String(7))

    __table_args__ = (
        UniqueConstraint("user_id", "title", name="uq_user_title"),
    )
