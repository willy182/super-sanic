import pybreaker

from src.shared.request.request_sanic import RequestCurlTo


class HttpRequest:

    def __init__(self):
        self.__http_request_handler = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=3)

    async def do_get_request(self, url, data=None, header=None):
        response = self.__http_request_handler.call_async(
            RequestCurlTo.curl,
            url,
            header
        )

        return response

    async def do_post_request(self, url, data=None, header=None):
        response = self.__http_request_handler.call_async(
            RequestCurlTo.curl_post,
            url,
            header,
            data
        )

        return response

    async def get_circuit_breaker(self):

        return self.__http_request_handler
