from aiogram_broadcaster import TextBroadcaster
from aiogram import Bot

from tgbot.config import Config


async def send_to_admins(bot: Bot, text: str) -> None:
    config: Config = bot.get('config')
    await TextBroadcaster(config.tg_bot.admin_ids, text=text, bot=bot).run()
