from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel

from .habit import HabitOutDTO


class IncrementProgressDTO(BaseModel):
    id: UUID
    increment_by: int


class UpdateProgressDTO(BaseModel):
    id: UUID
    current: int


class ProgresOutDTO(BaseModel):
    id: UUID
    user_id: UUID
    habit_id: UUID
    current: int
    updated_at: datetime
    created_date: date
    goal: int


class ProgressWithHabitOutDTO(ProgresOutDTO):
    habit: HabitOutDTO


class ListOfProgressesOutDTO(BaseModel):
    progresses: list[ProgresOutDTO]
    total_of_currents: int
    total_count: int


class ListOfProgressesWithHabitOutDTO(BaseModel):
    progresses: list[ProgressWithHabitOutDTO]
    habit_titles: list[str]
