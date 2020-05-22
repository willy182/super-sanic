from sanic import Blueprint
from sanic.response import json

from configs.config import Config
from helpers.validator.validator_jsonschema import JSONSchemaValidator
from src.shared.repository import Repository
from src.shared.request.http_request import HttpRequest
from src.shared.request.request_sanic import RequestSanicDict
from src.v1.area.repository.repository_postgres import AreaRepositoryPSQL
from src.v1.area.usecase.request_object_area import ListAllAreaRequestObject
from src.v1.area.usecase.usecase_area import ListAllAreaUsecase
from third_party.product.plankton import PlanktonV4Repository

bp_area_v1 = Blueprint('AreaV1', url_prefix='v1/area')

def _init_repo(db_manager, tracer):
    repo = Repository(default=AreaRepositoryPSQL(db_manager, tracer), **{
        'area': AreaRepositoryPSQL(db_manager, tracer),
        'plankton': PlanktonV4Repository(tracer),
    })

    return repo

@bp_area_v1.route('/', methods=['GET'])
async def index(request):
    request_dict = RequestSanicDict(request)
    validator = JSONSchemaValidator()

    adict = request_dict.query_to_dict()
    adict = validator.get_default_param(adict)

    repo_init = _init_repo(db_manager=request.app.db, tracer=request.app.tracer)
    use_cases = ListAllAreaUsecase(repo=repo_init)
    request_object = ListAllAreaRequestObject.from_dict(adict, validator=validator)
    response_object = await use_cases.execute(request_object)

    return json(response_object.value, status=Config.STATUS_CODES[response_object.type])