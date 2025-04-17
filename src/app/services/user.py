from sqlalchemy.orm import Session

from app.db import User
from app.exceptions import UniqueConstraintViolation
from app.repositories import UserRepository
from app.schema.user import CreateUserDTO, UserOutDTO
from app.utils.db import with_session


@with_session
def create_user(data: CreateUserDTO, session: Session) -> UserOutDTO:
    user_repository = UserRepository(session=session)
    if user_repository.get_by_telegram_chat_id(data.telegram_chat_id):
        raise UniqueConstraintViolation("User with this telegram chat id already exists")

    user = User(telegram_chat_id=data.telegram_chat_id)
    user = user_repository.create(user)
    return UserOutDTO(**user.__dict__)
