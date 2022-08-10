from aiogram import Dispatcher

from .admin import register_admin_handlers
from .start import register_start_handlers


def register_handlers(dp: Dispatcher) -> None:
    register_admin_handlers(dp)
    register_start_handlers(dp)
