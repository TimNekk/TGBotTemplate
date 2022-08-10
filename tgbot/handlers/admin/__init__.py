from aiogram import Dispatcher

from .send_all import register_send_all_handlers
from .ping import register_ping_handlers


def register_admin_handlers(dp: Dispatcher) -> None:
    register_send_all_handlers(dp)
    register_ping_handlers(dp)
