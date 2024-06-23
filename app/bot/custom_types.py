from typing import Protocol
from aiogram import Bot
from aiogram.types import Message
from .state import ChatState
from . import state
from .chat import ChatId


class SendMessage(Protocol):
    async def __call__(self, chat_id: ChatId, message_thread_id: int | None,message: str) -> Message: ...


class SaveState(Protocol):
    async def __call__(self, chat_state: ChatState) -> None: ...


class LoadState(Protocol):
    async def __call__(self, chat_id: ChatId, message_thread_id: int) -> ChatState: ...


class CreateState(Protocol):
    async def __call__(self, chat_id: ChatId, message_thread_id: int) -> None: ...
