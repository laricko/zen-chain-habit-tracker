import logging
from datetime import date, datetime, timedelta
from uuid import UUID

from pytz import timezone as pytz_timezone
from sqlalchemy.orm import Session

from app.db import Habit, Progress
from app.exceptions import EntityNotFound
from app.repositories import HabitRepository, ProgressRepository, UserRepository
from app.schemas import progress as progress_schemas
from app.schemas.habit import HabitOutDTO
from app.utils.db import with_session

logger = logging.getLogger(__name__)


@with_session
def create_progress_for_all_users(session: Session) -> None:
    """
    Daily task that create progress for all users and thier habit

    Creates progress according to whether habit daily or weekly or monthly
    """

    habit_repository = HabitRepository(session=session)
    progress_repository = ProgressRepository(session=session)

    last_progresses = progress_repository.get_all_users_last_progresses()
    last_progresses_habit_created_date_map = {progress.habit_id: progress.created_date for progress in last_progresses}
    habits_timezone = habit_repository.get_all_habits_with_user_timezone()
    progresses_to_create = []

    for habit, timezone in habits_timezone:
        last_date = last_progresses_habit_created_date_map.get(habit.id)
        if _should_create_progress(habit=habit, timezone=timezone, last_date=last_date):
            progresses_to_create.append(
                Progress(user_id=habit.user_id, habit_id=habit.id, current=0, goal=habit.goal)
            )

    progress_repository.bulk_create(progresses=progresses_to_create)
    logger.warning(f"Created {len(progresses_to_create)} progress records.")


@with_session
def increment_progress(data: progress_schemas.IncrementProgressDTO, session: Session) -> progress_schemas.ProgresOutDTO:
    progress_repository = ProgressRepository(session=session)

    progress = progress_repository.get_by_id(id=data.id)
    if not progress:
        raise EntityNotFound(f"Progress with {progress.id} not found")

    progress.current += data.increment_by
    progress = progress_repository.update(progress=progress)
    return progress_schemas.ProgresOutDTO(**progress.__dict__)


@with_session
def update_progress(id: UUID, data: progress_schemas.UpdateProgressDTO, session: Session) -> progress_schemas.ProgresOutDTO:
    progress_repository = ProgressRepository(session=session)

    progress = progress_repository.get_by_id(id=id)
    if not progress:
        raise EntityNotFound(f"Progress with {id} not found")

    progress.current = data.current
    progress = progress_repository.update(progress=progress)
    return progress_schemas.ProgresOutDTO(**progress.__dict__)


@with_session
def get_last_progress_by_user_id(user_id: UUID, session: Session) -> progress_schemas.ListOfProgressesWithHabitOutDTO:
    progress_repository = ProgressRepository(session=session)
    user_repository = UserRepository(session=session)

    if not user_repository.get_by_id(id=user_id):
        raise EntityNotFound(f"User with {user_id} not found")

    progresses_habits = progress_repository.get_last_by_user_id(user_id=user_id)
    progresses = []
    habit_titles = set()

    for progress, habit in progresses_habits:
        progresses.append(
            progress_schemas.ProgressWithHabitOutDTO(**progress.__dict__, habit=HabitOutDTO(**habit.__dict__))
        )
        habit_titles.add(habit.title.capitalize())

    return progress_schemas.ListOfProgressesWithHabitOutDTO(progresses=progresses, habit_titles=habit_titles)


@with_session
def get_progresses_by_habit_id(habit_id: UUID, session: Session) -> progress_schemas.ListOfProgressesOutDTO:
    habit_repository = HabitRepository(session=session)
    habit = habit_repository.get_by_id(id=habit_id)

    if not habit:
        raise EntityNotFound(f"Habit with {habit_id} id not found")

    progress_repository = ProgressRepository(session=session)
    progresses = progress_repository.get_by_habit_id(id=habit_id)

    total_count = 0
    total_of_currents = 0
    list_progresses = []

    for progress in progresses:
        list_progresses.append(progress_schemas.ProgresOutDTO(**progress.__dict__))
        total_count += 1
        total_of_currents += progress.current

    return progress_schemas.ListOfProgressesOutDTO(
        progresses=list_progresses,
        total_of_currents=total_of_currents,
        total_count=total_count
    )


def _should_create_progress(habit: Habit, timezone: str, last_date: date | None) -> bool:
    now_local = datetime.now(pytz_timezone(timezone)).date()

    if not last_date:
        return True

    if habit.frequency == "daily":
        return last_date < now_local
    elif habit.frequency == "weekly":
        return last_date <= now_local - timedelta(weeks=1)
    elif habit.frequency == "monthly":
        return last_date <= now_local.replace(day=1)
    return False
