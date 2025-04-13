from core.models.user import User
from core.schema.user import CreateUserDTO, UserOutDTO
from core.utils import crud


def create_user(data: CreateUserDTO) -> UserOutDTO:
    user = User(telegram_chat_id=data.telegram_chat_id)
    crud.create(user)
    return UserOutDTO(**user.model_dump())
