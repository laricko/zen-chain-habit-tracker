from uuid import UUID

from core import exceptions
from core.models.habit import Habit
from core.models.user import User
from core.schema.habit import CreateHabitDTO, HabitOutDTO, ListOfHabits
from core.utils import crud


def create_habit(data: CreateHabitDTO) -> HabitOutDTO:
    user_id = data.user_id
    user = crud.get_by_id(klass=User, id=user_id)
    if not user:
        raise exceptions.EntityNotFound(f"User with {user_id} not found")

    if crud.get_by_kwargs(klass=Habit, title=data.title, user_id=user_id):
        raise exceptions.UniqueConstraintViolation(f"User {user_id} already has a {data.title} habit")

    habit = Habit(**data.model_dump())
    crud.create(habit)
    return HabitOutDTO(**habit.model_dump())


def get_habits_by_user_id(user_id: UUID) -> ListOfHabits:
    user = crud.get_by_id(klass=User, id=user_id)
    if not user:
        raise exceptions.EntityNotFound(f"User with {user_id} not found")

    habits = crud.get_by_kwargs(klass=Habit, user_id=user_id)
    return ListOfHabits(habits=[HabitOutDTO(**habit.model_dump()) for habit in habits])
