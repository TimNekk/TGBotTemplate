from aiogram import types, Dispatcher

from tgbot.handlers.start import start
from tgbot.keyboards.inline import subscription
from tgbot.middlewares.callback_answer import do_not_answer
from tgbot.models.user_tg import UserTG


@do_not_answer()
async def _handle_subscription_callback(call: types.CallbackQuery, user: UserTG) -> None:
    await user.answer_callback_query(call.id, text="Доступ разрешен. Можете пользоваться ботом.")
    await user.delete_message(call.message.message_id)
    await start(call.message, user)


def register(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(_handle_subscription_callback, subscription.callback_data.filter())
