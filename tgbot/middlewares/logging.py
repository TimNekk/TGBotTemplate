from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types.base import TelegramObject
from loguru import logger


class LoggingMiddleware(BaseMiddleware):
    @staticmethod
    async def on_pre_process_update(update: TelegramObject, data: dict) -> None:
        logger.debug(update)
