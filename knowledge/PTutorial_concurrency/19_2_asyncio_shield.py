"""
Sometimes, you may want to inform users that a task is taking longer than expected after a certain amount of time but not cancel the task when a timeout is exceeded.

To do that, you can wrap the task with the asyncio.shield() function. The asyncio.shield() prevents the cancellation of a task. For example:

"""

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
        await asyncio.wait_for(asyncio.shield(task), timeout=MAX_TIMEOUT)
    except TimeoutError:
        print('The task took more than expected and will complete soon.')
        result = await task
        print(result)
        # In the exception handling section, we await for the task to be completed and print out the result.

asyncio.run(main())

"""
Calling API...
The task took more than expected and will complete soon.
2000
"""
