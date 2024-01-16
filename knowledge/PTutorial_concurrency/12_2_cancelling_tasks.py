"""
If you want to check every second if a task has been completed
and cancel it if an amount of time has passed, you can use a while loop:
"""
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

    time_elapsed = 0
    while not task.done():
        time_elapsed += 1
        await asyncio.sleep(1)
        print('Task has not completed, checking again in a second')
        if time_elapsed == 3:
            print('Cancelling the task...')
            task.cancel()
            break

    try:
        await task
    except CancelledError:
        print('Task has been cancelled.')


asyncio.run(main())

"""
Summary
Use the cancel() method of the Task object to cancel a task
await a canceled task will raise a CancelledError exception.
"""