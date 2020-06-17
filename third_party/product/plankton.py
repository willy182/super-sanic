import aiohttp
import asyncio

import requests
import uvloop

from configs.config_env import ConfigEnv
from src.shared.request.request_sanic import fetch_aio
from third_party.product.product import PlanktonRepository


class PlanktonV4RepositoryAsync(PlanktonRepository):

    def __init__(self, tracer):
        self.__tracer = tracer
        self.__url = ConfigEnv.PLANKTON_API_HOST
        self.__token = ConfigEnv.PLANKTON_API_BASIC_AUTH

    async def get_variant(self, uri):
        plankton_header = {
            "Authorization": self.__token,
            "Content-Type": "application/json"
        }

        url = '{}/v4{}'.format(self.__url, uri)

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        # timeout = aiohttp.ClientTimeout(total=50) # timeout dalam satuan menit
        async with aiohttp.ClientSession() as session:
            response = await fetch_aio(session, url, plankton_header, self.__tracer)

        return response


class PlanktonV4RepositorySync(PlanktonRepository):

    def __init__(self):
        self.__url = ConfigEnv.PLANKTON_API_HOST
        self.__token = ConfigEnv.PLANKTON_API_BASIC_AUTH


    def get_variant(self, uri):
        plankton_header = {
            "Authorization": self.__token,
            "Content-Type": "application/json"
        }

        url = '{}/v4{}'.format(self.__url, uri)

        response = requests.get(
            url,
            headers=plankton_header,
        )

        response = response.json()

        return response
