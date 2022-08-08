import sys

from loguru import logger


def setup(file_name: str = "log"):
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(f"logs/{file_name}.log", rotation="00:00", level="DEBUG")
