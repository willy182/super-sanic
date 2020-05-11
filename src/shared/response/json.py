from sanic.response import json

SERVED_BY = 'Shipment-Service-V3'


class Json(object):
    def __init__(self, properties=None, code=200):
        self.properties = properties
        self.code = code

    def format(self):
        return json(self.properties, headers={'X-Served-By': SERVED_BY}, status=self.code, sort_keys=False)

