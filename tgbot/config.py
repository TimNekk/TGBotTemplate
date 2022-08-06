from dataclasses import dataclass, fields
from typing import List, Optional

from aiogram.types import BotCommand
from environs import Env


@dataclass
class CommandInfo:
    command: str
    description: str
    alias: Optional[str] = None
    is_admin: bool = False
    bot_command: Optional[BotCommand] = None

    def __post_init__(self):
        self.bot_command = BotCommand(self.command, self.description)


@dataclass
class Commands:
    send_all: CommandInfo

    def __iter__(self):
        return (getattr(self, field.name) for field in fields(self))


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int
    uri: str = ""

    def __post_init__(self):
        self.uri = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class RedisConfig:
    host: str
    port: int
    password: str


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool
    commands: Commands


@dataclass
class Miscellaneous:
    log_file_name: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            commands=Commands(
                send_all=CommandInfo("send_all", "Рассылка", is_admin=True),
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
        ),
        misc=Miscellaneous(
            log_file_name=env.str("LOG_FILE_NAME")
        )
    )
