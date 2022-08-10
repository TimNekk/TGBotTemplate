import asyncio
import concurrent.futures
from typing import Any, Callable


async def run_blocking_io(func: Callable, *args: Any) -> Any:
    loop = asyncio.get_running_loop()

    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, func, *args
        )

    return result
