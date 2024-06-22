from datetime import datetime
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .custom_types import SendMessage, ChatId
from .constants import day_of_week, jobstore
from .messages import make_daily_messages
from .state import load_state, ChatState
import logging
from aiogram.utils.i18n import gettext as _


async def send_meeting_messages(chat_id: ChatId, send_message: SendMessage):
    chat_state = await load_state(chat_id=chat_id)
    await send_message(chat_id=chat_id, message=_("Meeting time!"))
    if not chat_state.joined_users:
        await send_message(chat_id=chat_id, message=_("Nobody has joined the meeting!"))
    else:
        for username in chat_state.joined_users:
            for message in make_daily_messages(username=username):
                await send_message(chat_id=chat_id, message=message)


def make_job_id(some_id: int):
    return str(some_id)


def schedule_meeting(
    meeting_time: datetime,
    chat_id: ChatId,
    scheduler: AsyncIOScheduler,
    send_message: SendMessage,
):
    scheduler.add_job(
        jobstore=jobstore,
        func=send_meeting_messages,
        id=make_job_id(chat_id),
        replace_existing=True,
        kwargs={"chat_id": chat_id, "send_message": send_message},
        trigger="cron",
        start_date=meeting_time,
        hour=meeting_time.hour,
        minute=meeting_time.minute,
        day_of_week=day_of_week,
        timezone=meeting_time.tzinfo,
        misfire_grace_time=42,
    )

    logging.info(scheduler.get_job(make_job_id(chat_id)))
