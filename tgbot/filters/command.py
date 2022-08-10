from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import CommandInfo


@dataclass
class CommandFilter(BoundFilter):
    key = 'command'
    command: CommandInfo

    async def check(self, obj: types.base.TelegramObject) -> bool:
        if not isinstance(obj, types.Message):
            raise NotImplementedError("CommandFilter can only be used with Message")
        message: types.Message = obj
        return message.text.startswith(f"/{self.command.command}") or self.command.alias == message.text
