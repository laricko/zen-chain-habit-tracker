from pydantic import BaseModel


class CreateUser(BaseModel):
    telegram_chat_id: str

    def execute(self):
        print(self.telegram_chat_id)
