from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Chat
from aiogram.utils.exceptions import ChatNotFound
from loguru import logger

from tgbot.keyboards.inline import subscription
from tgbot.models.user_tg import UserTG


class SubscriptionMiddleware(BaseMiddleware):
    channels: list[Chat] = []

    @classmethod
    async def setup_channels(cls, dp: Dispatcher, channels_ids: list[int]) -> None:
        for channel_id in channels_ids:
            try:
                cls.channels.append(await dp.bot.get_chat(chat_id=channel_id))
            except ChatNotFound:
                logger.warning(f"Chat {channel_id} not found")
                return

    async def on_process_message(self, message: Message, data: dict) -> None:
        user = data.get('user')
        if not user:
            raise KeyError(f"User not found in data")

        await self.check_subscriptions(message, user=user)

    async def on_process_callback_query(self, call: CallbackQuery, data: dict) -> None:
        user = data.get('user')
        if not user:
            raise KeyError(f"User not found in data")

        await self.check_subscriptions(call.message, user=user,
                                       call=call, callback_data=data.get("callback_data"))

    async def check_subscriptions(self,
                                  message: Message,
                                  user: UserTG,
                                  call: types.CallbackQuery | None = None,
                                  callback_data: dict | None = None) -> None:
        dispatcher = Dispatcher.get_current()

        channels_for_subscription = []
        for channel in self.channels:
            try:
                check_user = await dispatcher.bot.get_chat_member(chat_id=channel.id, user_id=message.chat.id)
            except ChatNotFound:
                logger.warning(f"Chat {channel.id} not found")
                continue

            if check_user.status not in ['creator', 'administrator', 'member']:
                channels_for_subscription.append(channel)

        if not channels_for_subscription:
            return

        text = f"<b>Для продолжения подпишитесь на {'каналы' if len(channels_for_subscription) > 1 else 'канал'}</b>"
        keyboard = subscription.keyboard(channels_for_subscription)

        if call and callback_data and subscription.callback_data.prefix in callback_data.values():
            text = f"Подпишитесь на {'все каналы' if len(channels_for_subscription) > 1 else 'канал'}!"
            await user.answer_callback_query(callback_query_id=call.id, text=text)
            if message.reply_markup != keyboard:
                await user.edit_message_text(text=text, message_id=message.message_id, reply_markup=keyboard)
            raise CancelHandler()

        await user.send_message(text, reply_markup=keyboard)
        raise CancelHandler()
