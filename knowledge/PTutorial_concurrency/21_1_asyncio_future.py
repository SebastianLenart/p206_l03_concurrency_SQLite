"""
When you use the await keyword with a future, you pause the future until it returns a value.
The following example shows how to use the future with await keyword:

"""
from asyncio import Future
import asyncio


async def plan(my_future):
    print('Planning my future...')
    await asyncio.sleep(1)
    my_future.set_result('Bright')


def create() -> Future:
    my_future = Future()
    asyncio.create_task(plan(my_future))
    return my_future


async def main():
    my_future = create()
    result = await my_future

    print(result)


asyncio.run(main())

"""
Planning my future...
Bright
"""

"""
First, define a coroutine that accepts a future and sets its value after 1 second:
Second, define a create() function that schedules the plan() coroutine as a task and returns a future object:
Third, call the create() function that returns a future, use the await keyword to wait for the future to return a result, and display it:
In practice, you’ll rarely need to create Future objects directly. However, you’ll use the Future objects returned from API. 
Therefore, it’s important to understand how the Future works.
"""

"""
A future is an object that returns a value in the future, not now.
Future, Coroutine, and Task are awaitable and their objects can be used with the await keyword
"""