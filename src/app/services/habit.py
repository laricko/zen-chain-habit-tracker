from uuid import UUID

from sqlalchemy.orm import Session

from app import exceptions
from app.db import Habit
from app.repositories import HabitRepository, UserRepository
from app.schema.habit import CreateHabitDTO, HabitOutDTO, ListOfHabits
from app.utils.db import with_session


@with_session
def create_habit(data: CreateHabitDTO, session: Session) -> HabitOutDTO:
    user_id = data.user_id
    user_repository = UserRepository(session=session)
    if not user_repository.get_by_id(id=user_id):
        raise exceptions.EntityNotFound(f"User with {user_id} not found")

    habit_repository = HabitRepository(session=session)
    if habit_repository.get_by_title_and_user_id(title=data.title, user_id=user_id):
        raise exceptions.UniqueConstraintViolation(f"User {user_id} already has a {data.title} habit")

    habit = Habit(**data.model_dump())
    habit = habit_repository.create(habit=habit)
    return HabitOutDTO(**habit.__dict__)


@with_session
def get_habits_by_user_id(user_id: UUID, session: Session) -> ListOfHabits:
    user_repository = UserRepository(session=session)
    if not user_repository.get_by_id(id=user_id):
        raise exceptions.EntityNotFound(f"User with {user_id} not found")

    habit_repository = HabitRepository(session=session)
    habits = habit_repository.get_by_user_id(user_id=user_id)
    return ListOfHabits(habits=[HabitOutDTO(**habit.__dict__) for habit in habits])
