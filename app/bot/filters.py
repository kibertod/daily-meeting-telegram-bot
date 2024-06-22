from aiogram.filters import Filter
from aiogram.types import Message, User
from .state import load_state


class HasMessageText(Filter):
    async def __call__(self, message: Message):
        match text := message.text:
            case str():
                return {"message_text": text}
        return False


class HasMessageUserUsername(Filter):
    async def __call__(self, message: Message):
        match user := message.from_user:
            case User():
                match user.username:
                    case str():
                        return {"username": user.username}
        return False


class HasChatState(Filter):
    async def __call__(self, message: Message):
        chat_state = await load_state(message.chat.id)
        return {"chat_state": chat_state}
