from helpers import helper
from schemas.json.loader import JSONSchemaLoader
from src.shared.request.request_object import ValidRequestObject, InvalidRequestObject


class ListAreaRequestObject(ValidRequestObject):

    def __init__(self, **kwargs):
        self.q = kwargs.get('q')
        self.limit = kwargs.get('limit')
        self.page = kwargs.get('page')

    @classmethod
    def from_dict(cls, adict, validator=None):
        # schema = JSONSchemaLoader.get("list_area_params")
        # message = JSONSchemaLoader.get("list_area_params_error_message")
        # if not validator.is_valid(adict=adict, schema=schema, messages=message):
        #     invalid_req = InvalidRequestObject()
        #     invalid_req.parse_error(errors=validator.get_errors())
        #     return invalid_req

        # data = validator.get_valid_data()

        # offset = (int(data['page']) * int(data['limit'])) - int(data['limit'])

        return ListAreaRequestObject(**{
            "q": adict.get('q'),
            "page": int(adict.get('page')),
            # "offset": offset,
            "limit": int(adict.get('limit')),
        })
