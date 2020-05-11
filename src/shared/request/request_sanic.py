import json
import requests
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
    @staticmethod
    def curl_post(url, headers, data):
        r = requests.post(
            url,
            headers=headers,
            data=data
        )

        return json.loads(r.text)

    @staticmethod
    def curl(url, headers):
        r = requests.get(
            url,
            headers=headers,
        )

        return json.loads(r.text)
