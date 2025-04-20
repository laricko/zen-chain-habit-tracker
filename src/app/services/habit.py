from uuid import UUID

from sqlalchemy.orm import Session

from app import exceptions
from app.db import Habit, Progress
from app.repositories import HabitRepository, ProgressRepository, UserRepository
from app.schemas.habit import CreateHabitDTO, HabitOutDTO, ListOfHabits
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

    progress_repository = ProgressRepository(session=session)
    progress_repository.create(
        Progress(
            user_id=habit.user_id,
            habit_id=habit.id,
            current=0,
            goal=data.goal,
        )
    )

    return HabitOutDTO(**habit.__dict__)


@with_session
def get_habits_by_user_id(user_id: UUID, session: Session) -> ListOfHabits:
    user_repository = UserRepository(session=session)
    if not user_repository.get_by_id(id=user_id):
        raise exceptions.EntityNotFound(f"User with {user_id} not found")

    habit_repository = HabitRepository(session=session)
    habits = habit_repository.get_by_user_id(user_id=user_id)
    return ListOfHabits(habits=[HabitOutDTO(**habit.__dict__) for habit in habits])


@with_session
def get_habit_by_title_and_user_id(title: str, user_id: UUID, session: Session) -> HabitOutDTO:
    user_repository = UserRepository(session=session)
    if not user_repository.get_by_id(id=user_id):
        raise exceptions.EntityNotFound(f"User with {user_id} not found")

    habit_repository = HabitRepository(session=session)
    habit = habit_repository.get_by_title_and_user_id(title=title, user_id=user_id)

    if not habit:
        raise exceptions.EntityNotFound(f"User {user_id} has no {title} habit")

    return HabitOutDTO(**habit.__dict__)


@with_session
def delete_habit(id: UUID, session: Session) -> None:
    habit_repository = HabitRepository(session=session)
    habit = habit_repository.get_by_id(id=id)

    if not habit:
        raise exceptions.EntityNotFound(f"Habit with {id} id not found")
    
    habit_repository.delete(id=id)
    return
