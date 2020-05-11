import asyncio
import time

import requests


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what, time.strftime('%X'))

async def get_url(delay, url):
    await asyncio.sleep(delay)
    r = requests.get(url)
    print(r.json()["description"], time.strftime('%X'))

async def main():
    print(f"started at {time.strftime('%X')}")
    task1 = asyncio.create_task(get_url(2, 'https://api.github.com/repos/psf/requests'))

    task2 = asyncio.create_task(say_after(0, 'hello'))

    task3 = asyncio.create_task(say_after(0, 'world'))

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2
    await task3
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())