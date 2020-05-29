import aiohttp

import requests

from configs.config_env import ConfigEnv
from src.shared.request.request_sanic import fetch_aio
from third_party.product.product import PlanktonRepository


class PlanktonV4Repository(PlanktonRepository):

    def __init__(self, tracer):
        # self.__http_client = http_client
        self.__tracer = tracer
        self.__url = ConfigEnv.PLANKTON_API_HOST
        self.__token = ConfigEnv.PLANKTON_API_BASIC_AUTH


    async def get_variant(self, uri):
        plankton_header = {
            "Authorization": self.__token,
            "Content-Type": "application/json"
        }

        url = '{}/v4{}'.format(self.__url, uri)

        # response = requests.get(
        #     url,
        #     headers=plankton_header,
        # )
        #
        # response = response.json()

        timeout = aiohttp.ClientTimeout(total=10) # timeout dalam satuan menit
        async with aiohttp.ClientSession(timeout=timeout) as session:
            response = await fetch_aio(session, url, plankton_header, timeout, self.__tracer)

        return response
