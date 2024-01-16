import asyncio
import time


async def call_api(message, result=1000, delay=3):
    print(message)
    await asyncio.sleep(delay)
    return result


async def main():
    start = time.perf_counter()

    task_1 = asyncio.create_task(
        call_api('Get stock price of GOOG...', 300)
    )

    task_2 = asyncio.create_task(
        call_api('Get stock price of APPL...', 400)
    )

    price = await task_1
    print(price)

    price = await task_2
    print(price)

    end = time.perf_counter()
    print(f'It took {round(end-start,0)} second(s) to complete.')


asyncio.run(main())

"""
Get stock price of GOOG...
Get stock price of APPL...
300
400
It took 3.0 second(s) to complete.

"""