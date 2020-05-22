import asyncio
import time

import grequests
import requests


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what, time.strftime('%X'))

async def get_url(delay, url):
    # await asyncio.sleep(delay)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic cGxhbmt0b246UHJAJDNUeTAtLTREIT1TNG42X192M05kT3I='
    }
    r = grequests.get(url, headers=headers)
    time.strftime('%X')
    # print(r.json()["data"][0]["fullname"], time.strftime('%X'))
    return r

async def main():
    print(f"started at {time.strftime('%X')}")
    url1 = get_url(0, 'https://plankton-api.bhinneka.com/v4/variants?noCache=true')
    url2 = get_url(0, 'https://plankton-api.bhinneka.com/v4/variants?include=product,offers&page[number]=1&page[size]=100&filter[status]=published&channel=b2b&noCache=true')
    tasks = []
    tasks.append(url1)
    tasks.append(url2)
    grequests.map(tasks)
    print(url1)

    # task2 = asyncio.create_task(say_after(0, 'hello'))
    #
    # task3 = asyncio.create_task(say_after(0, 'world'))

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    # await task0
    # await task1
    # await task2
    # await task3
    print(f"finished at {time.strftime('%X')}")

# asyncio.run(main())