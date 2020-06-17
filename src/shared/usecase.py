import traceback
from src.shared.response import response_object as ro
from sanic.log import logger


class UseCaseAsync(object):
    async def execute(self, request_object):

        if not request_object:
            return ro.ResponseFailure.build_from_invalid_request_object(request_object)
        try:
            return await self.process_request(request_object)

        except Exception as exc:

            logger.error("{}: {} . System: {}".format(exc.__class__.__name__, "{}".format(exc), traceback.format_exc()))

            return ro.ResponseFailure.build_system_error(message=traceback.format_exc())

    def process_request(self, request_object):
        raise NotImplementedError("process_request() not implemented by UseCase class")


class UseCaseSync(object):
    def execute(self, request_object):

        if not request_object:
            return ro.ResponseFailure.build_from_invalid_request_object(request_object)
        try:
            return self.process_request(request_object)

        except Exception as exc:

            logger.error("{}: {} . System: {}".format(exc.__class__.__name__, "{}".format(exc), traceback.format_exc()))

            return ro.ResponseFailure.build_system_error(message=traceback.format_exc())

    def process_request(self, request_object):
        raise NotImplementedError("process_request() not implemented by UseCase class")