from aiogram import Dispatcher

from .admin import AdminFilter
from .command import CommandFilter


def register(dp: Dispatcher) -> None:
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(CommandFilter)
