import aiohttp
import requests

from configs.config_env import ConfigEnv
from src.shared.request.request_sanic import fetch_aio
from third_party.product.product import PlanktonRepository


class PlanktonV4RepositoryAsync(PlanktonRepository):

    def __init__(self, tracer, session):
        self.__tracer = tracer
        self.__session = session
        self.__url = ConfigEnv.PLANKTON_API_HOST
        self.__token = ConfigEnv.PLANKTON_API_BASIC_AUTH

    async def get_variant(self, uri):
        plankton_header = {
            "Authorization": self.__token,
            "Content-Type": "application/json"
        }

        url = '{}/v4{}'.format(self.__url, uri)

        response = await fetch_aio(self.__session, url, plankton_header, self.__tracer)

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
