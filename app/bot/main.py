import asyncio
import logging
import sys
from .constants import AppCommands
import argparse
from .messages import make_help_message, make_daily_messages
from . import bot
from .settings import Settings
from pydantic import ValidationError


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title="subcommands", description="bot commands", dest="command"
    )

    subparsers.add_parser(
        AppCommands.print_bot_message, help="print the bot help message"
    )

    subparsers.add_parser(
        AppCommands.print_meeting_messages,
        help="print sample meeting messages",
    )
    subparsers.add_parser(AppCommands.start, help="run the bot")

    args = parser.parse_args()

    match args.command:
        case AppCommands.print_bot_message:
            print(make_help_message())
        case AppCommands.print_meeting_messages:
            for message in make_daily_messages(username="username"):
                print(message)
        case AppCommands.start:
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)

            try:
                settings = Settings()
                asyncio.run(bot.main(settings=settings))
            except ValidationError as e:
                print(e)


if __name__ == "__main__":
    main()
