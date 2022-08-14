from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


callback_data = CallbackData("subscription")


def _make_callback_data() -> str:
    return callback_data.new()


def keyboard(channels_for_subscription: list[types.Chat]) -> InlineKeyboardMarkup:
    _keyboard = InlineKeyboardMarkup()

    for channel in channels_for_subscription:
        _keyboard.add(InlineKeyboardButton(text=channel.title, url=channel.invite_link))

    _keyboard.add(InlineKeyboardButton(text="Проверить", callback_data=_make_callback_data()))

    return _keyboard
