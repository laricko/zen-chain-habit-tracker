from uuid import UUID

from pydantic import BaseModel

from core.models.habit import HabitFrequency


class CreateHabitDTO(BaseModel):
    user_id: UUID
    title: str
    goal: int
    frequency: HabitFrequency


class HabitOutDTO(CreateHabitDTO):
    id: UUID


class ListOfHabits(BaseModel):
    habits: list[HabitOutDTO]
