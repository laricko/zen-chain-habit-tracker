from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Habit(Base):
    __tablename__ = "habit"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String(255))
    goal: Mapped[int]
    frequency: Mapped[str] = mapped_column(String(7))

    __table_args__ = (
        UniqueConstraint("user_id", "title", name="uq_user_title"),
    )
