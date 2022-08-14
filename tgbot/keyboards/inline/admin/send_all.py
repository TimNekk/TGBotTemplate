from enum import auto

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.misc.string_enum import StringEnum


class Action(StringEnum):
    BUTTONS = auto()
    SEND = auto()
    CANCEL = auto()


setup_callback_data = CallbackData("send_all", "action")


def _make_setup_callback_data(action: Action) -> str:
    return setup_callback_data.new(action=action)


def setup_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text="Изменить кнопки ⚙️",
                                      callback_data=_make_setup_callback_data(Action.BUTTONS)))

    keyboard.add(InlineKeyboardButton(text="Отправить 📩",
                                      callback_data=_make_setup_callback_data(Action.SEND)))

    keyboard.add(InlineKeyboardButton(text="Отмена ❌",
                                      callback_data=_make_setup_callback_data(Action.CANCEL)))

    return keyboard


def broadcast_message_keyboard(buttons: list[list[str]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for button in buttons:
        keyboard.add(InlineKeyboardButton(text=button[0],
                                          url=button[1]))

    return keyboard
