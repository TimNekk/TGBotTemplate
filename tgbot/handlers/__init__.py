from aiogram import Dispatcher

from tgbot.handlers import admin
from tgbot.handlers import start
from tgbot.handlers import subscription
from tgbot.handlers import block


def register(dp: Dispatcher) -> None:
    admin.register(dp)
    start.register(dp)
    subscription.register(dp)
    block.register(dp)
