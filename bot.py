import ssl

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.storage import BaseStorage
from aiogram.types import AllowedUpdates

from aiogram.utils import executor
from loguru import logger

from tgbot.config import load_config, Config
from tgbot import filters
from tgbot import handlers
from tgbot import middlewares
from tgbot.misc import logging
from tgbot.models import db
from tgbot.models.user_tg import UserTG
from tgbot.services.broadcasting import send_to_admins
from tgbot.services.setting_commands import set_bot_command


def setup_logging(config: Config) -> None:
    logging.setup(config.log.file_name, config.log.rotation, config.log.retention)


def get_aiogram_storage(config: Config) -> BaseStorage:
    if config.tg_bot.use_redis:
        return RedisStorage2(host=config.redis.host,
                             port=config.redis.port,
                             password=config.redis.password,
                             pool_size=config.redis.pool_size)

    return MemoryStorage()


def setup_dispatcher(config: Config, storage: BaseStorage | None) -> Dispatcher:
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    bot['config'] = config
    dp = Dispatcher(bot, storage=storage)
    return dp


async def setup_storages(config: Config, bot: Bot) -> None:
    logger.info("Setting up storages...")
    await db.on_startup(config.db.uri)
    UserTG.bot = bot


async def register_middlewares_filters_handlers(dp: Dispatcher, config: Config) -> None:
    logger.info("Registering middlewares, filters, handlers, dialogs...")
    await middlewares.register(dp, config)
    filters.register(dp)
    handlers.register(dp)


async def setup_webhook(bot: Bot, config: Config) -> None:
    ssl_cert = open(config.tg_bot.ssl.cert_file_path, 'rb').read()
    logger.info(f"Set webhook on {config.tg_bot.webhook.url}")
    await bot.set_webhook(
        url=config.tg_bot.webhook.url,
        certificate=ssl_cert
    )


async def on_startup(dp: Dispatcher) -> None:
    config: Config = dp.bot["config"]

    await setup_storages(config, dp.bot)

    await send_to_admins(dp.bot, "🟡 Бот запускается")

    if config.tg_bot.use_webhook:
        await setup_webhook(dp.bot, config)

    await register_middlewares_filters_handlers(dp, config)
    await set_bot_command(dp.bot, config)

    await send_to_admins(dp.bot, "🟢 Бот запущен")


async def on_shutdown(dp: Dispatcher) -> None:
    await send_to_admins(dp.bot, "🔴 Бот остановлен")
    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()
    await db.on_shutdown()
    await dp.bot.delete_webhook()


def main() -> None:
    config = load_config(".env")
    setup_logging(config)
    logger.info("Starting bot")

    aiogram_storage = get_aiogram_storage(config)
    dp = setup_dispatcher(config, aiogram_storage)

    if config.tg_bot.use_webhook:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(config.tg_bot.ssl.cert_file_path,
                                    config.tg_bot.ssl.key_file_path)

        logger.info(f"Start webhook on webhook_path={config.tg_bot.webhook.path}, "
                    f"host={config.tg_bot.web_server.host}, port={config.tg_bot.web_server.port}")
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.tg_bot.webhook.path,
            host=config.tg_bot.web_server.host,
            port=config.tg_bot.web_server.port,
            ssl_context=ssl_context,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=config.tg_bot.skip_updates,
        )
    else:
        executor.start_polling(dp,
                               on_startup=on_startup,
                               on_shutdown=on_shutdown,
                               allowed_updates=[
                                   AllowedUpdates.MESSAGE,
                                   AllowedUpdates.CALLBACK_QUERY,
                                   AllowedUpdates.MY_CHAT_MEMBER
                               ])


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
        raise SystemExit(0)
