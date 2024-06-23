from pathlib import Path
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from . import handlers
from .state import ChatState
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .state import load_state
from .meeting import schedule_meeting
from .custom_types import SendMessage, ChatId
from .settings import Settings
from . import db
from apscheduler.jobstores.memory import MemoryJobStore
from pytz import utc
from .constants import jobstore
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import FSMI18nMiddleware


def init_scheduler(settings: Settings) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=utc, jobstores={jobstore: MemoryJobStore()})
    scheduler.start()
    return scheduler


async def restore_scheduled_jobs(
    scheduler: AsyncIOScheduler, send_message: SendMessage
):
    chat_states = await ChatState.find_all().to_list()

    for chat_state in chat_states:
        if chat_state.meeting_time:
            schedule_meeting(
                meeting_time=chat_state.meeting_time,
                chat_id=chat_state.chat_id,
                message_thread_id=chat_state.message_thread_id,
                scheduler=scheduler,
                send_message=send_message,
            )


# async def on_startup():
#     bot_commands = [
#         BotCommand()
#     ]

async def main(settings: Settings) -> None:
    await db.main(settings=settings)

    dp = Dispatcher()

    i18n = I18n(path="locales", default_locale="en", domain="messages")
    fsmi18n = FSMI18nMiddleware(i18n)
    fsmi18n.setup(router=dp)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    async def send_message(chat_id: ChatId, message_thread_id:int | None, message: str):
        return await bot.send_message(chat_id=chat_id, message_thread_id=message_thread_id, text=message)

    scheduler = init_scheduler(settings=settings)
    await restore_scheduled_jobs(scheduler=scheduler, send_message=send_message)

    router = handlers.make_router(scheduler=scheduler, send_message=send_message)

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)
