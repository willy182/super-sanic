from helpers import helper
from schemas.json.loader import JSONSchemaLoader
from src.shared.request.request_object import ValidRequestObject, InvalidRequestObject


class ListAllAreaRequestObject(ValidRequestObject):

    def __init__(self, **kwargs):
        self.q = kwargs.get('q')
        self.limit = kwargs.get('limit')
        self.offset = kwargs.get('offset')
        self.page = kwargs.get('page')

    @classmethod
    def from_dict(cls, adict, validator=None):
        schema = JSONSchemaLoader.get("all_area_get_params")
        if not validator.is_valid(adict=adict, schema=schema):
            invalid_req = InvalidRequestObject()
            invalid_req.parse_error(errors=validator.get_errors())
            return invalid_req

        data = validator.get_valid_data()

        offset = (int(data['page']) * int(data['limit'])) - int(data['limit'])

        return ListAllAreaRequestObject(**{
            "q": helper.get_value('q', data, ''),
            "page": int(data['page']),
            "offset": offset,
            "limit": int(data['limit']),
        })
