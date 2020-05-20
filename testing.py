import asyncio
import time

import requests


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what, time.strftime('%X'))

async def get_url(delay, url):
    await asyncio.sleep(delay)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic cGxhbmt0b246UHJAJDNUeTAtLTREIT1TNG42X192M05kT3I='
    }
    r = requests.get(url, headers=headers)
    print(r.json()["data"][0]["fullname"], time.strftime('%X'))

async def main():
    print(f"started at {time.strftime('%X')}")
    # task0 = asyncio.create_task(get_url(2, 'https://plankton-api.bhinneka.com/v4/variants?filter[skuNo]=3316920142&noCache=true'))

    task1 = asyncio.create_task(get_url(1, 'https://plankton-api.bhinneka.com/v4/variants?filter[skuNo]=3316920142&noCache=true'))

    task2 = asyncio.create_task(say_after(0, 'hello'))

    task3 = asyncio.create_task(say_after(0, 'world'))

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2
    await task3
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
