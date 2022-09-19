from typing import Any, Callable

from aiogram import types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

from tgbot.models.user_tg import UserTG


def answer_setup(text: str | None = None,
                 show_alert: bool | None = None,
                 url: str | None = None,
                 cache_time: int | None = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        setattr(func, 'answer_text', text)
        setattr(func, 'answer_show_alert', show_alert)
        setattr(func, 'answer_url', url)
        setattr(func, 'answer_cache_time', cache_time)

        return func

    return decorator


def do_not_answer() -> Callable:
    def decorator(func: Callable) -> Callable:
        setattr(func, 'do_not_answer', True)
        return func

    return decorator


class CallbackAnswerMiddleware(BaseMiddleware):
    @staticmethod
    async def on_process_callback_query(call: types.CallbackQuery, data: dict[Any, Any]) -> None:
        handler = current_handler.get()

        if getattr(handler, 'do_not_answer', None):
            return

        user = data.get('user')
        if not user or not isinstance(user, UserTG):
            logger.exception('CallbackAnswerMiddleware can not find user in data')
            return

        await user.answer_callback_query(callback_query_id=call.id,
                                         text=getattr(handler, 'answer_text', None),
                                         show_alert=getattr(handler, 'answer_show_alert', None),
                                         url=getattr(handler, 'answer_url', None),
                                         cache_time=getattr(handler, 'answer_cache_time', None))
