from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config


@dataclass
class AdminFilter(BoundFilter):
    key = 'is_admin'
    is_admin: bool

    async def check(self, obj: types.base.TelegramObject) -> bool:
        config: Config = obj.bot.get('config')
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin
