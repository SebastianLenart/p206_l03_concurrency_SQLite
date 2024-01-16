"""
The asyncio.wait() function runs an iterable of awaitables objects and blocks until a specified condition

asyncio.wait(aws, *, timeout=None, return_when=ALL_COMPLETED)
The asyncio.wait() function has the following parameters:

aws is iterable of awaitable objects that you want to run concurrently.
timeout (either int or float) specifies a maximum number of seconds to wait before returning the result.
return_when indicates when the function should return. The return_when accepts one of the constants in the table below.
FIRST_COMPLETED	Return when all awaitables are complete or canceled.
FIRST_EXCEPTION	Return when any awaitable is complete by raising an exception. If no awaitable raises an exception, the FIRST_EXCEPTION is equivalent to ALL_COMPLETED.
ALL_COMPLETED	Return when all awaitables are complete or cancelled.

Note that these constants are in the asyncio library so you can reference them like asyncio.FIRST_COMPLETED

The asyncio.wait() returns two sets:

done, pending = await asyncio.wait(aws)
Code language: Python (python)
done is a set of awaitables that are done.
pending is a set of awaitables that are pending.
"""