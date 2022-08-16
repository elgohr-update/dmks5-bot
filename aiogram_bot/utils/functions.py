from datetime import timedelta
from typing import Union

from babel.dates import format_timedelta
from loguru import logger
from aiogram.utils import exceptions
from aiogram import types

from aiogram_bot.misc import i18n
from aiogram_bot.models.chat import Chat

_ = i18n.gettext


async def apply_restriction(message: types.Message, chat: Chat, duration: Union[timedelta, int]) -> bool:
    try:  # Apply restriction
        await message.chat.restrict(
            message.reply_to_message.from_user.id, can_send_messages=False, until_date=duration
        )
        logger.info(
            "User {user} restricted by {admin} for {duration}",
            user=message.reply_to_message.from_user.id,
            admin=message.from_user.id,
            duration=duration,
        )
    except exceptions.BadRequest as e:
        logger.error("Failed to restrict chat member: {error!r}", error=e)
        return False

    await message.reply_to_message.answer(
        _("<b>Read-only</b> activated for user {user}. Duration: {duration}").format(
            user=message.reply_to_message.from_user.get_mention(),
            duration=format_timedelta(
                duration, locale=chat.language, granularity="seconds", format="short"
            ),
        )
    )
    return True
