from aiogram import Bot
from aiogram.types import BotCommandScopeChat, BotCommandScopeDefault
from aiogram.utils.exceptions import ChatNotFound
from loguru import logger

from tgbot.config import Config


async def set_bot_command(bot: Bot, config: Config) -> None:
    await bot.set_my_commands(
        commands=[command.bot_command for command in config.tg_bot.commands if not command.is_admin],
        scope=BotCommandScopeDefault()
    )

    for admin_id in config.tg_bot.admin_ids:
        try:
            await bot.set_my_commands(
                commands=[command.bot_command for command in config.tg_bot.commands],
                scope=BotCommandScopeChat(admin_id)
            )
        except ChatNotFound:
            logger.warning(f"Admin with id {admin_id} not found")
