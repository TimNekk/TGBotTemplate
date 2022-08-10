from typing import Any

from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class EnvironmentMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        self.kwargs = kwargs

    async def pre_process(self, obj: types.base.TelegramObject, data: dict[Any, Any], *args: Any) -> None:
        data.update(**self.kwargs)
