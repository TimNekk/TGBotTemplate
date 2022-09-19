from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram_broadcaster import MessageBroadcaster
import validators

from tgbot.config import Config
from tgbot.keyboards.inline.admin import send_all
from tgbot.models.user import User
from tgbot.models.user_tg import UserTG
from tgbot.states import SendAllState


async def _handle_send_all(message: types.Message, user: UserTG, state: FSMContext) -> None:
    text = "<b>Отправьте сообщение для рассылки</b>"
    initial_message = await user.send_message(text)

    await SendAllState.waiting_for_message.set()
    await state.update_data(initial_message_id=initial_message.message_id)


async def _confirm_send(message: types.Message, user: UserTG, state: FSMContext) -> None:
    data = await state.get_data()
    initial_message_id: int = data.get("initial_message_id")

    await user.delete_message(initial_message_id)
    await user.delete_message(message.message_id)

    broadcast_message = await message.send_copy(user.id)
    await user.send_message("<b>Все пользователям будет отправлено сообщение 👆</b>",
                            reply_markup=send_all.setup_keyboard())

    await SendAllState.waiting_for_confirm.set()
    await state.update_data(broadcast_message_id=broadcast_message.message_id)


async def _ask_to_change_buttons(call: types.CallbackQuery, user: UserTG, state: FSMContext) -> None:
    text = """
Введите <b>ВСЕ</b> кнопки в формате:

<code>Текст кнопки1|ссылка кнопки1</code>
<code>Текст кнопки2|ссылка кнопки2</code>

Пример:
<code>Подписаться на канал|https://t.me/joinchat/XXXXXXXX</code>
<code>Зайти в гугл|https://google.com</code>

"""
    buttons_message = await user.send_message(text)
    await SendAllState.waiting_for_buttons.set()
    await state.update_data(buttons_message_id=buttons_message.message_id)


async def _change_buttons(message: types.Message, user: UserTG, state: FSMContext) -> None:
    data = await state.get_data()
    buttons_message_id: int = data.get("buttons_message_id")
    broadcast_message_id: int = data.get("broadcast_message_id")

    await user.delete_message(buttons_message_id)
    await user.delete_message(message.message_id)

    buttons = list(filter(lambda button: len(button) == 2 and validators.url(button[1]),
                          [[button_args.strip() for button_args in button.split("|")]
                           for button in message.text.split("\n")]))

    if buttons:
        keyboard = send_all.broadcast_message_keyboard(buttons)
        await user.edit_message_reply_markup(broadcast_message_id, reply_markup=keyboard)
        await state.update_data(keyboard=keyboard)

    await SendAllState.waiting_for_confirm.set()


async def _cancel(call: types.CallbackQuery, state: FSMContext, user: UserTG) -> None:
    data = await state.get_data()
    broadcast_message_id: int = data.get("broadcast_message_id")
    await state.finish()

    await user.delete_message(call.message.message_id)
    await user.delete_message(broadcast_message_id)


async def _start_broadcast(call: types.CallbackQuery, user: UserTG, state: FSMContext) -> None:
    data = await state.get_data()
    broadcast_message_id: int = data.get("broadcast_message_id")
    keyboard: types.InlineKeyboardMarkup = data.get("keyboard")
    await state.finish()

    users_id = [user_id[0] for user_id in await User.select("id").where(User.is_banned == False).gino.all()]

    await user.send_message(f'Рассылка на всех пользователей (<b>{len(users_id)}</b>) началась!')
    broadcast_message = await call.bot.forward_message(call.message.chat.id, call.message.chat.id, broadcast_message_id)
    await user.delete_message(broadcast_message.message_id)
    await MessageBroadcaster(chats=users_id, message=broadcast_message, reply_markup=keyboard).run()

    await user.send_message("<b>Рассылка закончилась!</b>")


def register(dp: Dispatcher) -> None:
    config: Config = dp.bot.get("config")
    dp.register_message_handler(_handle_send_all,
                                command=config.tg_bot.commands.send_all,
                                is_admin=True)
    dp.register_message_handler(_confirm_send,
                                content_types=ContentType.ANY,
                                is_admin=True,
                                state=SendAllState.waiting_for_message)
    dp.register_callback_query_handler(_ask_to_change_buttons,
                                       send_all.setup_callback_data.filter(action=send_all.Action.BUTTONS()),
                                       is_admin=True,
                                       state=SendAllState.waiting_for_confirm)
    dp.register_callback_query_handler(_cancel,
                                       send_all.setup_callback_data.filter(action=send_all.Action.CANCEL()),
                                       is_admin=True,
                                       state=SendAllState.waiting_for_confirm)
    dp.register_message_handler(_change_buttons,
                                is_admin=True,
                                state=SendAllState.waiting_for_buttons)
    dp.register_callback_query_handler(_start_broadcast,
                                       send_all.setup_callback_data.filter(action=send_all.Action.SEND()),
                                       is_admin=True,
                                       state=SendAllState.waiting_for_confirm)
