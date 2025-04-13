from enum import StrEnum, auto
from uuid import UUID

from .base import Base


class HabitFrequency(StrEnum):
    daily = auto()
    weekly = auto()
    monthly = auto()


class Habit(Base):
    user_id: UUID
    title: str
    goal: int
    frequency: HabitFrequency
