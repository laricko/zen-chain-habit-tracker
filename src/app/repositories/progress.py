from uuid import UUID

from sqlalchemy import desc, select, update
from sqlalchemy.orm import Session

from app.db import Progress


class ProgressRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def bulk_create(self, progresses: list[Progress]) -> list[Progress]:
        self.session.bulk_save_objects(progresses)
        self.session.flush()

    def get_all_users_last_progresses(self) -> list[Progress]:
        stmt = (
            select(Progress)
            .distinct(Progress.user_id, Progress.habit_id)
            .order_by(Progress.user_id, Progress.habit_id, desc(Progress.created_date))
        )

        return self.session.execute(stmt).scalars().all()

    def update(self, progress: Progress) -> Progress:
        stmt = update(Progress).where(Progress.id == progress.id).values(**progress.__dict__).returning(Progress)
        return self.session.scalars(stmt).one()

    def get_by_id(self, id: UUID) -> Progress | None:
        return self.session.get(Progress, id)

    def get_by_user_id(self, user_id: UUID) -> list[Progress]:
        stmt = select(Progress).where(Progress.user_id == user_id)
        return self.session.scalars(stmt).all()
