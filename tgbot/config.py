from dataclasses import dataclass, fields
from datetime import time, timedelta, datetime
from typing import List, Optional, Generator

from aiogram.types import BotCommand
from environs import Env


@dataclass
class CommandInfo:
    command: str
    description: str
    alias: Optional[str] = None
    is_admin: bool = False
    bot_command: Optional[BotCommand] = None

    def __post_init__(self) -> None:
        self.bot_command = BotCommand(self.command, self.description)


@dataclass
class Commands:
    send_all: CommandInfo
    ping: CommandInfo

    def __iter__(self) -> Generator[CommandInfo, None, None]:
        return (getattr(self, field.name) for field in fields(self))


@dataclass
class WebhookConfig:
    host: str
    port: int
    path: str

    def __post_init__(self) -> None:
        self.path = f"/{self.path}"
        self.url = f"{self.host}:{self.port}{self.path}"


@dataclass
class WebServerConfig:
    host: str
    port: int


@dataclass
class SSLConfig:
    cert_file_name: str
    key_file_name: str

    def __post_init__(self) -> None:
        directory = "certs/"
        self.cert_file_path = f"{directory}{self.cert_file_name}"
        self.key_file_path = f"{directory}{self.key_file_name}"


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int
    uri: str = ""

    def __post_init__(self) -> None:
        self.uri = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class RedisConfig:
    host: str
    port: int
    password: str
    pool_size: int


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool
    skip_updates: bool
    use_webhook: bool
    webhook: WebhookConfig
    web_server: WebServerConfig
    ssl: SSLConfig
    commands: Commands
    subscription_channels_ids: List[int]


@dataclass
class LogConfig:
    file_name: str
    rotation: time
    retention: timedelta


@dataclass
class Miscellaneous:
    pass


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig
    log: LogConfig
    misc: Miscellaneous


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            subscription_channels_ids=list(map(int, env.list("SUBSCRIPTION_CHANNELS_IDS"))),
            commands=Commands(
                send_all=CommandInfo("send_all", "Запустить рассылку", is_admin=True),
                ping=CommandInfo("ping", "Узнать пинг", is_admin=True),
            ),
            use_webhook=env.bool("USE_WEBHOOK"),
            skip_updates=env.bool("SKIP_UPDATES"),
            webhook=WebhookConfig(
                host=env.str('WEBHOOK_HOST'),
                port=env.str("WEBHOOK_PORT"),
                path=env.str('WEBHOOK_PATH')
            ),
            web_server=WebServerConfig(
                host=env.str('WEB_SERVER_HOST'),
                port=env.int('WEB_SERVER_PORT')
            ),
            ssl=SSLConfig(
                cert_file_name=env.str('SSL_CERT_FILE_NAME'),
                key_file_name=env.str('SSL_KEY_FILE_NAME')
            )
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            port=env.int('DB_PORT'),
        ),
        redis=RedisConfig(
            host=env.str('REDIS_HOST'),
            password=env.str('REDIS_PASS'),
            port=env.int('REDIS_PORT'),
            pool_size=env.int('REDIS_POOL_SIZE'),
        ),
        log=LogConfig(
            file_name=env.str('LOG_FILE_NAME'),
            rotation=datetime.strptime(env.str('LOG_ROTATION'), '%H:%M').time(),
            retention=timedelta(days=env.int('LOG_RETENTION')),
        ),
        misc=Miscellaneous()
    )
