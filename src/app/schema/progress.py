from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class IncrementProgressDTO(BaseModel):
    id: UUID
    increment_by: int


class UpdateProgressDTO(BaseModel):
    id: UUID
    current: int


class ProgressOutDTO(BaseModel):
    id: UUID
    user_id: UUID
    habit_id: UUID
    current: int
    updated_at: datetime
    created_date: date
    goal: int


class ListOfProgressOutDTO(BaseModel):
    progresses: list[ProgressOutDTO]
