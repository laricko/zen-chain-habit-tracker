from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.user import User


class UserRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()
        return user

    def get_by_id(self, id: UUID) -> User | None:
        return self.session.get(User, id)

    def get_by_telegram_chat_id(self, telegram_chat_id: int) -> User | None:
        stmt = select(User).where(User.telegram_chat_id == telegram_chat_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()
