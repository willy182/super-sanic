import logging
from configs.config import Config

logger = logging.getLogger(__name__)


class ResponseSuccess(object):

    def __init__(self, value=None, type=Config.SUCCESS):
        self.value = value
        self.type = type

class CommonResponse(object):

    def __init__(self, message, type):
        self.message = self._format_message(message)
        self.type = type

    def _format_message(self, message):
        if isinstance(message, Exception):
            # log
            logger.error(message)

            return "{}: {}".format(message.__class__.__name__, "{}".format(message))
        return message

    @property
    def value(self):
        status = True
        if Config.STATUS_CODES[self.type] != 200 and Config.STATUS_CODES[self.type] != 201:
            status = False

        return {'success': status, 'code': Config.STATUS_CODES[self.type], 'message': self.message}

    def __bool__(self):
        return False

    @classmethod
    def build_common_message(cls, message=None, code=None):
        return cls(message, code)

    @classmethod
    def build_from_invalid_request_object(cls, invalid_request_object):
        message = "\n".join(["{}: {}".format(err['parameter'], err['message'])
                             for err in invalid_request_object.errors])
        return cls.build_common_message(message, Config.PARAMETERS_ERROR)
