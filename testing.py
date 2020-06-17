import asyncio
import time
from datetime import datetime

import aiohttp


async def say_after(delay, what):
    await asyncio.sleep(delay)
    now = datetime.now()
    print(what, now.time())

async def get_url(delay, url):
    await asyncio.sleep(delay)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic cGxhbmt0b246UHJAJDNUeTAtLTREIT1TNG42X192M05kT3I='
    }
    timeout = aiohttp.ClientTimeout(total=20)  # timeout dalam satuan menit
    async with aiohttp.ClientSession(timeout=timeout) as session:
        response = await fetch_aio(session, url, headers, timeout)

    print(url, response)

async def fetch_aio(session, url, headers, timeout):
    now1 = datetime.now()
    tt1 = now1.time()
    print(url, tt1)

    async with session.get(url, headers=headers, timeout=timeout) as response:
        res = await response.json()

    now2 = datetime.now()
    tt2 = now2.time()
    print(url, tt2)

    return res

async def main():
    print(f"started at {time.strftime('%X')}")

    await asyncio.gather(
        get_url(0, 'https://plankton-api.bhinneka.com/v4/variants?noCache=true'),
        say_after(0, 'lahloh'),
        get_url(0, 'https://plankton-api.bhinneka.com/v4/variants?include=product,offers&page[number]=1&page[size]=100&filter[status]=published&channel=b2b&noCache=true'),
    )
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())