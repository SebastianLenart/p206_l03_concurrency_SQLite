"""
Sometimes, you may want to run multiple asynchronous operations and get the results once they are complete.
To do that you can use the asyncio.gather() function:

gather(*aws, return_exceptions=False) -> Future[tuple[()]]
Code language: Python (python)
The asyncio.gather() function has two parameters:

aws is a sequence of awaitable objects. If any object in the aws is a coroutine, the asyncio.gather() function will
automatically schedule it as a task.
return_exceptions is False by default. If an exception occurs in an awaitable object, it is immediately propagated to
the task that awaits on asyncio.gather(). Other awaitables will continue to run and won’t be canceled.
The asyncio.gather() returns the results of awaitables as a tuple with the same order as you pass the awaitables
to the function.

If the return_exceptions is True. The asyncio.gather() will add the exception if any to the result and not propagate
the exception to the caller.


"""