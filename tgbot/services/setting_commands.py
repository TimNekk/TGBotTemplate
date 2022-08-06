from aiogram import Bot
from aiogram.types import BotCommandScopeChat, BotCommandScopeDefault

from tgbot.config import Config


async def set_bot_command(bot: Bot, config: Config):
    await bot.set_my_commands(
        commands=[command.bot_command for command in config.tg_bot.commands if not command.is_admin],
        scope=BotCommandScopeDefault()
    )

    for admin_id in config.tg_bot.admin_ids:
        await bot.set_my_commands(
            commands=[command.bot_command for command in config.tg_bot.commands],
            scope=BotCommandScopeChat(admin_id)
        )
