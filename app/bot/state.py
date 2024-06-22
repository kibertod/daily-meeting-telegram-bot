from typing import Optional, Annotated
from datetime import datetime
from beanie import Document, Indexed
import pymongo
from zoneinfo import ZoneInfo
from .chat import ChatId
from .language import Language


class ChatState(Document):
    language: Language = Language.default
    meeting_time: Optional[datetime] = None
    chat_id: Annotated[ChatId, Indexed(index_type=pymongo.ASCENDING)]
    joined_users: set[str] = set()


async def create_state(chat_id: ChatId) -> ChatState:
    return await ChatState(chat_id=chat_id).create()


async def load_state(chat_id: ChatId) -> ChatState:
    match chat_state := await ChatState.find_one(ChatState.chat_id == chat_id):
        case ChatState():
            return chat_state
        case _:
            return await create_state(chat_id=chat_id)


async def save_state(chat_state: ChatState) -> None:
    await chat_state.save()
