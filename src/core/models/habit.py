from enum import StrEnum, auto
from uuid import UUID

from pydantic import BaseModel


class HabitFrequency(StrEnum):
    daily = auto()
    weekly = auto()
    monthly = auto()


class Habit(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    goal: int
    frequency: HabitFrequency
