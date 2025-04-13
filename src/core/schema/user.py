from uuid import UUID

from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    telegram_chat_id: int


class UserOutDTO(CreateUserDTO):
    id: UUID
