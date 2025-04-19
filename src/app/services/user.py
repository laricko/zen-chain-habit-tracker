import logging

from sqlalchemy.orm import Session

from app.db import User
from app.exceptions import EntityNotFound, UniqueConstraintViolation
from app.repositories import UserRepository
from app.schemas.user import CreateUserDTO, UserOutDTO
from app.utils.db import with_session

logger = logging.getLogger(__name__)


@with_session
def create_user(data: CreateUserDTO, session: Session) -> UserOutDTO:
    user_repository = UserRepository(session=session)
    if user_repository.get_by_telegram_chat_id(data.telegram_chat_id):
        raise UniqueConstraintViolation("User with this telegram chat id already exists")

    user = User(telegram_chat_id=data.telegram_chat_id)
    user = user_repository.create(user)
    logger.info(f"New user with {user.telegram_chat_id} telegram id just created.")
    return UserOutDTO(**user.__dict__)


@with_session
def get_user_by_telegram_chat_id(telegram_chat_id: int, session: Session) -> UserOutDTO:
    user_repository = UserRepository(session=session)
    user = user_repository.get_by_telegram_chat_id(telegram_chat_id=telegram_chat_id)

    if not user:
        raise EntityNotFound(f"User with telegram chat id {telegram_chat_id} not found")

    return UserOutDTO(**user.__dict__)
