from aiogram import types, Dispatcher

from tgbot.handlers.start import start
from tgbot.keyboards.inline import subscription
from tgbot.middlewares.callback_answer import do_not_answer
from tgbot.models.user_tg import UserTG


@do_not_answer()
async def handle_subscription_callback(call: types.CallbackQuery, user: UserTG) -> None:
    await call.answer(text="Доступ разрешен. Можете пользоваться ботом.")
    await call.message.delete()
    await start(call.message, user)


def register_subscription_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(handle_subscription_callback, subscription.callback_data.filter())
