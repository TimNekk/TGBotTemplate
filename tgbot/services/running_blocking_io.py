import asyncio
import concurrent.futures


async def run_blocking_io(func, *args):
    loop = asyncio.get_running_loop()

    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, func, *args
        )

    return result
