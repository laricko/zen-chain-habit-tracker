from enum import StrEnum, auto
from uuid import UUID

from pydantic import BaseModel


class HabitFrequency(StrEnum):
    daily = auto()
    weekly = auto()
    monthly = auto()


class CreateHabitDTO(BaseModel):
    user_id: UUID
    title: str
    goal: int
    frequency: HabitFrequency


class HabitOutDTO(CreateHabitDTO):
    id: UUID


class ListOfHabits(BaseModel):
    habits: list[HabitOutDTO]
