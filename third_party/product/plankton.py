import time

import aiohttp
from datetime import datetime

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
        # print('get_variant', time.strftime('%X'))
        now1 = datetime.now()
        tt1 = now1.time()
        # print(tt1)

        plankton_header = {
            "Authorization": self.__token,
            "Content-Type": "application/json"
        }

        url = '{}/v4{}'.format(self.__url, uri)

        # response = await self.__http_client.do_get_request(
        #     url=url,
        #     header=plankton_header
        # )

        async with aiohttp.ClientSession() as session:
            response = await fetch_aio(session, url, plankton_header, self.__tracer)

        return response
