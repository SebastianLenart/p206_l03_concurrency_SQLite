import asyncio
import time


async def call_api(message, result=1000, delay=3):
    print(message)
    await asyncio.sleep(delay)
    return result


async def main():
    start = time.perf_counter()

    price = await call_api('Get stock price of GOOG...', 300)
    print(price)

    price = await call_api('Get stock price of APPL...', 400)
    print(price)

    end = time.perf_counter()
    print(f'It took {round(end-start,0)} second(s) to complete.')

asyncio.run(main())


"""
In other words, we use async and await to write asynchronous code but can’t run it concurrently. 
To run multiple operations concurrently, we’ll need to use something called tasks

"""