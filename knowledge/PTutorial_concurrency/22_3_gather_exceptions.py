import asyncio


class APIError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


async def call_api(message, result, delay=3):
    print(message)
    await asyncio.sleep(delay)
    return result


async def call_api_failed():
    await asyncio.sleep(1)
    raise APIError('API failed')


async def main():
    a, b, c = await asyncio.gather(
        call_api('Calling API 1 ...', 100, 1),
        call_api('Calling API 2 ...', 200, 2),
        call_api_failed(),
        return_exceptions=True
    )
    print(a, b, c)


asyncio.run(main())

"""
The asyncio.gather() runs multiple asynchronous operations, wraps a coroutine as a task, 
and returns a tuple of results in the same order of awaitables.
Set return_exceptions to True to allow errors to be returned as results.
"""