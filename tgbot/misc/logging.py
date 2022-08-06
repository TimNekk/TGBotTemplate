from loguru import logger


def setup(file_name: str = "log"):
    logger.add(f"logs/{file_name}.log", rotation="00:00", level="DEBUG")
