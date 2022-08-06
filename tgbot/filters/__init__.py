from aiogram import Dispatcher

from .admin import AdminFilter
from .command import CommandFilter


def register_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(CommandFilter)
