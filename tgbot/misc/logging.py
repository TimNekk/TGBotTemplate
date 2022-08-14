import logging
from datetime import time, timedelta
import sys

import aiogram_broadcaster
import gino
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame = logging.currentframe()
        depth = 2
        while frame.f_code.co_filename == logging.__file__:
            if frame.f_back:
                frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup(file_name: str = "log.log", rotation: time = time(), retention: timedelta = timedelta(days=3)) -> None:
    # Disable some packages logging
    logging.getLogger(aiogram_broadcaster.__name__).setLevel(logging.FATAL)
    logging.getLogger(gino.__name__).setLevel(logging.FATAL)

    # Setup loguru
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(f"logs/{file_name}", rotation=rotation, retention=retention, level="DEBUG")

    # Send default logging to loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
