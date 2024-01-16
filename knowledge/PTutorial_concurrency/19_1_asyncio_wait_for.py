import asyncio
from asyncio.exceptions import TimeoutError


async def call_api(message, result=1000, delay=3):
    print(message)
    await asyncio.sleep(delay)
    return result


async def main():
    task = asyncio.create_task(
        call_api('Calling API...', result=2000, delay=5)
    )

    MAX_TIMEOUT = 3
    try:
        await asyncio.wait_for(task, timeout=MAX_TIMEOUT)
    except TimeoutError:
        print('The task was cancelled due to a timeout')

asyncio.run(main())


"""
Calling API...
The task was cancelled due to a timeout
"""