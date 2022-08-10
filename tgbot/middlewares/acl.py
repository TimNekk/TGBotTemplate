from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.models.user_tg import UserTG


class ACLMiddleware(BaseMiddleware):
    @staticmethod
    async def set_data(telegram_user: types.User, data: dict, deep_link: str | None = None) -> None:
        user = await UserTG.get(telegram_user.id)

        if user is None:
            user = UserTG(
                id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                deep_link=deep_link if deep_link else None
            )
            await user.create()
        elif user.is_banned:
            await user.update(is_banned=False).apply()

        data["user"] = user
        data["deep_link"] = deep_link

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        await self.set_data(message.from_user, data, deep_link=message.get_args())

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict) -> None:
        await self.set_data(callback_query.from_user, data)
