from jsonschema import Draft4Validator, exceptions, Draft6Validator, Draft7Validator
from helpers.validator.ivalidator import Validator

class JSONSchemaValidator(Validator):#pragma: no cover
    def __init__(self):
        self.__errors = []
        self.__data = []

        super(JSONSchemaValidator, self).__init__()

    def is_valid(self, adict, schema, messages=None, draft=4):
        def trace_error_value(error):
            if len(error.path) != 0: return (error.path[-1], error.message)
            return ('keyError', error.message)

        if draft == 4:
            self.__errors = dict(
                trace_error_value(e) for e in sorted(
                    Draft4Validator(schema).iter_errors(adict), key=exceptions.by_relevance()
                )
            )

        if draft == 6:
            self.__errors = dict(
                trace_error_value(e) for e in sorted(
                    Draft6Validator(schema).iter_errors(adict), key=exceptions.by_relevance()
                )
            )

        if draft == 7:
            self.__errors = dict(
                trace_error_value(e) for e in sorted(
                    Draft7Validator(schema).iter_errors(adict), key=exceptions.by_relevance()
                )
            )


        if len(self.__errors) > 0 and messages:
            self.__errors = self.remap_error_message(self.__errors, messages)

        self.__data = adict if len(self.__errors) == 0 else []

        return len(self.__errors) == 0

    def get_errors(self):
        return self.__errors

    def get_valid_data(self):
        return self.__data

    def get_default_param(self, adict):
        if 'page' not in adict:
            adict['page'] = '1'

        if 'limit' not in adict:
            adict['limit'] = '10'

        if 'sortBy' not in adict:
            adict['sortBy'] = 'desc'

        if 'orderBy' not in adict:
            adict['orderBy'] = 'id'

        return adict

    def remap_error_message(self, errors, messages):
        if len(errors) > 1 and 'keyError' in errors:
            del errors['keyError']

        for key in errors:
            try:
                for value in messages['properties'][key]:
                    if value["contains"] in errors[key]:
                        errors[key] = value["replaceWith"]
                        break
            except Exception:
                pass
        return errors
