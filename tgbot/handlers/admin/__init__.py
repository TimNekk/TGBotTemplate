from aiogram import Dispatcher

from tgbot.handlers.admin import send_all
from tgbot.handlers.admin import ping


def register(dp: Dispatcher) -> None:
    send_all.register(dp)
    ping.register(dp)
