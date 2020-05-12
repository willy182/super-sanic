from configs.config_env import ConfigEnv
from third_party.product.product import PlanktonRepository


class PlanktonV4Repository(PlanktonRepository):

    def __init__(self, http_client):
        self.__http_client = http_client
        self.__url = ConfigEnv.PLANKTON_API_HOST
        self.__token = ConfigEnv.PLANKTON_API_BASIC_AUTH


    async def get_variant(self, uri):

        plankton_header = {
            "Authorization": self.__token,
            "Content-Type": "application/json"
        }

        url = '{}/v4{}'.format(self.__url, uri)

        response = await self.__http_client.do_get_request(
            url=url,
            header=plankton_header
        )

        return response
