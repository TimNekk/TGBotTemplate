from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart

from tgbot.models.user_tg import UserTG


async def start(message: types.Message, user: UserTG) -> None:
    text = f"""
<b>Привет{f', {user.info}' if user.info else ''}!</b>
"""

    await user.send_message(text)


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(start, CommandStart())
