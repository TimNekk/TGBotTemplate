from enum import auto

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.misc.string_enum import StringEnum


send_all_callback_data = CallbackData("send_all", "action")


class SendAllAction(StringEnum):
    BUTTONS = auto()
    SEND = auto()
    CANCEL = auto()


def make_send_all_callback_data(action: SendAllAction):
    return send_all_callback_data.new(action=action)


def send_all_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text="Изменить кнопки ⚙️",
                                      callback_data=make_send_all_callback_data(SendAllAction.BUTTONS)))

    keyboard.add(InlineKeyboardButton(text="Отправить 📩",
                                      callback_data=make_send_all_callback_data(SendAllAction.SEND)))

    keyboard.add(InlineKeyboardButton(text="Отмена ❌",
                                      callback_data=make_send_all_callback_data(SendAllAction.CANCEL)))

    return keyboard


def broadcast_message_keyboard(buttons: list[list[str, str]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for button in buttons:
        keyboard.add(InlineKeyboardButton(text=button[0],
                                          url=button[1]))

    return keyboard
