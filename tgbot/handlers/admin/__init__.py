from aiogram import Dispatcher

from .send_all import register_send_all_handlers


def register_admin_handlers(dp: Dispatcher):
    register_send_all_handlers(dp)
