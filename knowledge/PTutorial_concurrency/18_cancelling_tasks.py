import asyncio
from asyncio import CancelledError


async def call_api(message, result=1000, delay=3):
    print(message)
    await asyncio.sleep(delay)
    return result


async def main():
    task = asyncio.create_task(
        call_api('Calling API...', result=2000, delay=5)
    )

    if not task.done():
        print('Cancelling the task...')
        task.cancel()

    try:
        await task
    except CancelledError:
        print('Task has been cancelled.')


asyncio.run(main())

"""
Cancelling the task...
Task has been cancelled
"""