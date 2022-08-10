from datetime import time, timedelta
import sys

from loguru import logger


def setup(file_name: str = "log", rotation: time = time(), retention: timedelta = timedelta(days=3)) -> None:
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(f"logs/{file_name}.log", rotation=rotation, retention=retention, level="DEBUG")
