import json
import requests

from datetime import datetime
from tornado import gen

from helpers.helper import get_result_subtraction_time
from src.shared.request.irequest import Request


class RequestSanicDict(Request):
    def __init__(self, request):
        self.request = request
        super(RequestSanicDict, self).__init__()

    def form_to_dict(self):
        dict_d = {}
        try:
            for key in dict(self.request.form):
                dict_d[key] = self.request.form.get(key, '')
        except Exception as e:
            pass

        return dict_d

    def json_to_dict(self):
        dict_d = {}
        try:
            dict_d.update(self.request.json)
        except Exception as e:
            pass

        return dict_d

    def json_to_list(self):
        list_d = []
        try:
            list_d = self.request.json
        except Exception as e:
            pass

        return list_d

    def query_to_dict(self):
        dict_d = {}
        try:
            dict_d.update(self.request.query_args)
        except Exception as e:
            pass

        return dict_d

    def parse_all_to_dict(self):
        dict_d = {}
        try:
            dict_d.update(self.json_to_dict())
            dict_d.update(self.form_to_dict())
            dict_d.update(self.query_to_dict())
            dict_d.update(self.header_to_dict())
            dict_d.update(self.remote_addr(as_dict=True))
        except Exception as e:
            pass

        return dict_d

    def header_to_dict(self):
        return self.request.headers

    def remote_addr(self, as_dict=False):
        if as_dict:
            return {"remote_addr": self.request.ip}
        return self.request.ip


class RequestCurlTo:
    @gen.coroutine
    def curl_post(url, headers, data):
        r = requests.post(
            url,
            headers=headers,
            data=data
        )

        return json.loads(r.text)

    @gen.coroutine
    def curl(url, headers):
        r = requests.get(
            url,
            headers=headers,
        )

        return json.loads(r.text)

async def fetch_aio(session, url, headers, tracer):
    now1 = datetime.now()
    tt1 = now1.time()

    with tracer.start_span(url) as span:
        async with session.get(url, headers=headers) as response:
            res = await response.json()

        now2 = datetime.now()
        tt2 = now2.time()
        str_time = get_result_subtraction_time(tt1, tt2)
        span.log_kv({'process_time': str_time})
        span.set_tag('url', url)

    return res