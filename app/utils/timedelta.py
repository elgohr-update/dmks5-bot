import datetime
import typing

from aiogram import types

MODIFIERS = {
    "w": datetime.timedelta(weeks=1),
    "d": datetime.timedelta(days=1),
    "h": datetime.timedelta(hours=1),
    "m": datetime.timedelta(minutes=1),
    "s": datetime.timedelta(seconds=1),
}


class TimedeltaParseError(Exception):
    pass


def parse_timedelta(value: str) -> datetime.timedelta:
    try:
        value, modifier = value[:-1], value[-1:]
        result = datetime.timedelta()

        result += int(value) * MODIFIERS[modifier]
    except OverflowError:
        raise TimedeltaParseError("Timedelta value is too large")
    except (KeyError, ValueError):
        raise TimedeltaParseError("Wrong format")

    return result


async def parse_timedelta_from_message(
    message: types.Message
) -> typing.Optional[datetime.timedelta]:
    _, *args = message.text.split()

    if args:  # Parse custom duration
        try:
            duration = parse_timedelta(args[0])
        except TimedeltaParseError:
            await message.reply("Failed to parse duration")
            return
        if duration <= datetime.timedelta(seconds=30) and message.from_user.id == 52346052:
            message.reply("Да как же ты заебал уже, на, на тебе ебучий таймаут.")

        return duration

    return datetime.timedelta(minutes=15)
