import logging
from datetime import date, timedelta
from uuid import UUID

from sqlalchemy.orm import Session

from app.db import Progress
from app.exceptions import EntityNotFound
from app.repositories import HabitRepository, ProgressRepository, UserRepository
from app.schema.progress import (
    IncrementProgressDTO,
    ListOfProgressOutDTO,
    ProgressOutDTO,
    UpdateProgressDTO,
)
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
    habits = habit_repository.get_all()
    progresses_to_create = []

    for habit in habits:
        last_date = last_progresses_habit_created_date_map.get(habit.id)
        if _should_create_progress(habit, last_date):
            progresses_to_create.append(
                Progress(user_id=habit.user_id, habit_id=habit.id, current=0)
            )

    progress_repository.bulk_create(progresses=progresses_to_create)
    logger.info(f"Created {len(progresses_to_create)} progress records.")


@with_session
def increment_progress(data: IncrementProgressDTO, session: Session) -> ProgressOutDTO:
    progress_repository = ProgressRepository(session=session)

    progress = progress_repository.get_by_id(id=data.id)
    if not progress:
        raise EntityNotFound(f"Progress with {progress.id} not found")

    progress.current += data.increment_by
    progress = progress_repository.update(progress=progress)
    return ProgressOutDTO(progress.__dict__)


@with_session
def update_progress(data: UpdateProgressDTO, session: Session) -> ProgressOutDTO:
    progress_repository = ProgressRepository(session=session)

    progress = progress_repository.get_by_id(id=data.id)
    if not progress:
        raise EntityNotFound(f"Progress with {progress.id} not found")

    progress.current = data.current
    progress = progress_repository.update(progress=progress)
    return ProgressOutDTO(progress.__dict__)


@with_session
def get_progress_by_user_id(user_id: UUID, session: Session) -> ListOfProgressOutDTO:
    progress_repository = ProgressRepository(session=session)
    user_repository = UserRepository(session=session)

    if not user_repository.get_by_id(id=user_id):
        raise EntityNotFound(f"User with {user_id} not found")

    progresses = progress_repository.get_by_user_id(user_id=user_id)
    return ListOfProgressOutDTO(progresses=[ProgressOutDTO(**progress.__dict__) for progress in progresses])


def _should_create_progress(habit, last_date: date | None) -> bool:
    if not last_date:
        return True

    if habit.frequency == "daily":
        return last_date < date.today()
    elif habit.frequency == "weekly":
        return last_date <= date.today() - timedelta(weeks=1)
    elif habit.frequency == "monthly":
        return last_date <= date.today().replace(day=1)
    return False
