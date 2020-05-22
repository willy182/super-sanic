from sanic import Blueprint
from sanic.response import json

from configs.config import Config
from helpers.validator.validator_jsonschema import JSONSchemaValidator
from src.shared.repository import Repository
from src.shared.request.http_request import HttpRequest
from src.shared.request.request_sanic import RequestSanicDict
from src.v1.area.repository.repository_postgres import AreaRepositoryPSQL
from src.v1.expeditions.repository.repository_postgres import ExpeditionsRepositoryPSQL
from src.v1.expeditions.usecase.request_object_expedtions import ListAreaRequestObject
from src.v1.expeditions.usecase.usecase_expeditions import ListExpeditionUsecase
from third_party.product.plankton import PlanktonV4Repository

bp_expeditions_v1 = Blueprint('ExpeditionsV1', url_prefix='v1/expeditions')

def _init_repo(db_manager, tracer):
    # http_client = HttpRequest()
    repo = Repository(default=ExpeditionsRepositoryPSQL(db_manager, tracer), **{
        'expedition': ExpeditionsRepositoryPSQL(db_manager, tracer),
        'area': AreaRepositoryPSQL(db_manager, tracer),
        'plankton': PlanktonV4Repository(tracer),
    })

    return repo

@bp_expeditions_v1.route('/', methods=['GET'])
async def index(request):
    request_dict = RequestSanicDict(request)
    validator = JSONSchemaValidator()

    adict = request_dict.query_to_dict()
    adict = validator.get_default_param(adict)

    repo_init = _init_repo(db_manager=request.app.db, tracer=request.app.tracer)
    use_cases = ListExpeditionUsecase(repo=repo_init)
    request_object = ListAreaRequestObject.from_dict(adict, validator=validator)
    response_object = await use_cases.execute(request_object)

    return json(response_object.value, status=Config.STATUS_CODES[response_object.type])