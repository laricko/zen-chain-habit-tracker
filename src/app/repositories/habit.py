from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import Habit


class HabitRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, habit: Habit) -> Habit:
        self.session.add(habit)
        self.session.flush()
        return habit

    def get_by_id(self, id: UUID) -> Habit | None:
        return self.session.get(Habit, id)

    def get_by_title_and_user_id(self, title: str, user_id: UUID) -> Habit | None:
        stmt = select(Habit).where(func.lower(Habit.title) == title.lower(), Habit.user_id == user_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_user_id(self, user_id: UUID) -> list[Habit]:
        stmt = select(Habit).where(Habit.user_id == user_id)
        return self.session.execute(stmt).scalars().all()

    def get_all(self) -> list[Habit]:
        stmt = select(Habit)
        return self.session.execute(stmt).scalars().all()
