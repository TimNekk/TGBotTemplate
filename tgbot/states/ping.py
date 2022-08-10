from aiogram.dispatcher.filters.state import State, StatesGroup


class PingState(StatesGroup):
    waiting_for_ping = State()
