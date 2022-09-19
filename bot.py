from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import AllowedUpdates
from asyncio import run
from loguru import logger

from tgbot.config import load_config
from tgbot import filters
from tgbot import handlers
from tgbot import middlewares
from tgbot.misc import logging
from tgbot.models import db
from tgbot.models.user_tg import UserTG
from tgbot.services.broadcasting import send_to_admins
from tgbot.services.setting_commands import set_bot_command


async def main() -> None:
    config = load_config(".env")

    logging.setup(config.log.file_name, config.log.rotation, config.log.retention)
    logger.info("Starting bot")

    if config.tg_bot.use_redis:
        storage = RedisStorage2(host=config.redis.host,
                                port=config.redis.port,
                                password=config.redis.password,
                                pool_size=config.redis.pool_size)
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    bot['config'] = config
    dp = Dispatcher(bot, storage=storage)

    await db.on_startup(config.db.uri)
    UserTG.bot = bot

    await middlewares.register(dp, config)
    filters.register(dp)
    handlers.register(dp)

    await set_bot_command(bot, config)
    await send_to_admins(bot, "Бот запущен")

    try:
        await dp.start_polling(allowed_updates=[
            AllowedUpdates.MESSAGE,
            AllowedUpdates.CALLBACK_QUERY,
            AllowedUpdates.CHAT_MEMBER,
            AllowedUpdates.MY_CHAT_MEMBER
        ])
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await (await bot.get_session()).close()
        await db.on_shutdown()


if __name__ == '__main__':
    try:
        run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
        raise SystemExit(0)
