"""
Finally, call the asyncio.wait() function to run the tasks inside a while loop.
If all the tasks are complete, the pending will be empty, and the while loop will exit. In each iteration,
we get the completed task from the done set and display the result:

"""

import asyncio
from asyncio import create_task


class APIError(Exception):
    pass


async def call_api(message, result=100, delay=3, raise_exception=False):
    print(message)
    await asyncio.sleep(delay)
    if raise_exception:
        raise APIError
    else:
        return result


async def main():
    task_1 = create_task(call_api('calling API 1...', result=1, delay=1))
    task_2 = create_task(call_api('calling API 2...', result=2, delay=2))
    task_3 = create_task(call_api('calling API 3...', result=3, delay=3))

    pending = (task_1, task_2, task_3)

    while pending:
        done, pending = await asyncio.wait(
            pending,
            return_when=asyncio.FIRST_COMPLETED
        )
        result = done.pop().result()
        print(result)


asyncio.run(main())
"""
calling API 1...
calling API 2...
calling API 3...
1
2
3
"""