from uuid import UUID

from sqlalchemy import and_, case, desc, func, select, update
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import over

from app.db import Habit, Progress


class ProgressRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def bulk_create(self, progresses: list[Progress]) -> None:
        self.session.bulk_save_objects(progresses)
        self.session.flush()

    def create(self, progress: Progress) -> Progress:
        self.session.add(progress)
        self.session.flush()
        return progress

    def get_all_users_last_progresses(self) -> list[Progress]:
        stmt = (
            select(Progress)
            .distinct(Progress.user_id, Progress.habit_id)
            .order_by(Progress.user_id, Progress.habit_id, desc(Progress.created_date))
        )

        return self.session.execute(stmt).scalars().all()

    def update(self, progress: Progress) -> Progress:
        stmt = update(Progress).where(Progress.id == progress.id).values(**progress.__dict__).returning(Progress)
        return self.session.execute(stmt).one()

    def get_by_id(self, id: UUID) -> Progress | None:
        return self.session.get(Progress, id)

    def get_by_habit_id(self, id: UUID) -> list[Progress]:
        stmt = (
            select(Progress)
            .where(Progress.habit_id == id)
            .order_by(desc(Progress.created_date))
            .limit(30)
        )
        return self.session.execute(stmt).scalars().all()

    def get_last_by_user_id(self, user_id: UUID) -> list[tuple[Progress, Habit]]:
        habit_alias = aliased(Habit)
        progress_alias = aliased(Progress)

        row_number = func.row_number().over(
            partition_by=progress_alias.habit_id,
            order_by=desc(progress_alias.created_date)
        ).label("row_number")

        max_row = case(
            (habit_alias.frequency == 'daily', 4),
            (habit_alias.frequency == 'weekly', 2),
            (habit_alias.frequency == 'monthly', 1),
            else_=0
        ).label("max_row")

        subquery = (
            select(
                progress_alias.id.label("progress_id"),
                habit_alias.id.label("habit_id"),
                row_number,
                max_row
            )
            .join(habit_alias, habit_alias.id == progress_alias.habit_id)
            .where(progress_alias.user_id == user_id)
        ).subquery()

        stmt = (
            select(Progress, Habit)
            .join(Habit, Habit.id == Progress.habit_id)
            .join(subquery, and_(
                Progress.id == subquery.c.progress_id,
                Habit.id == subquery.c.habit_id
            ))
            .where(subquery.c.row_number <= subquery.c.max_row)
            .order_by(desc(Progress.created_date))
        )

        return self.session.execute(stmt).all()
