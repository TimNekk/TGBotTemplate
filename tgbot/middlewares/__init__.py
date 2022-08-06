from aiogram import Dispatcher
from ..config import Config

from .acl import ACLMiddleware
from .logging import LoggingMiddleware
from .environment import EnvironmentMiddleware
from .callback_answer import CallbackAnswerMiddleware
from .throttling import ThrottlingMiddleware


def register_middlewares(dp: Dispatcher, config: Config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(LoggingMiddleware())
    dp.setup_middleware(CallbackAnswerMiddleware())
    dp.setup_middleware(ThrottlingMiddleware())
