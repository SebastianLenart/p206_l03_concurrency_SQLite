import asyncio


async def call_api(message, result, delay=3):
    print(message)
    await asyncio.sleep(delay)
    return result


async def main():
    a, b = await asyncio.gather(
        call_api('Calling API 1 ...', 100, 1),
        call_api('Calling API 2 ...', 200, 2)
    )
    print(a, b)


asyncio.run(main())
"""
Calling API 1 ...
Calling API 2 ...
100 200
"""

"""
The first coroutine takes 1 second and returns 100 while the second coroutine takes 2 seconds and returns 100.

After 2 seconds, the gather returns the result as a tuple that contains the result of the first and second coroutines.

Note that a is 100 and b is 200 which are the results of the corresponding coroutine that we pass to the asyncio.gather() function.
"""