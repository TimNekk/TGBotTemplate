from aiogram.dispatcher.filters.state import State, StatesGroup


class SendAllState(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirm = State()
    waiting_for_buttons = State()
