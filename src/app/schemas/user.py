from uuid import UUID

from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    telegram_chat_id: int
    timezone: str | None


class UserOutDTO(CreateUserDTO):
    id: UUID
    timezone: str


class UpdateUserDTO(BaseModel):
    timezone: str
