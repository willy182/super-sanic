from sanic import Blueprint
from sanic.response import json

from configs.config import Config
from helpers.validator.validator_jsonschema import JSONSchemaValidator
from src.shared.repository import Repository
from src.shared.request.request_sanic import RequestSanicDict
from src.asynchronous.area.repository.repository_postgres import AreaRepositoryPSQL
from src.asynchronous.expeditions.repository.repository_postgres import ExpeditionsRepositoryPSQL
from src.asynchronous.expeditions.usecase.request_object_expedtions import ListAreaRequestObject
from src.asynchronous.expeditions.usecase.usecase_expeditions import ListExpeditionUsecase
from third_party.product.plankton import PlanktonV4RepositoryAsync

bp_expeditions_async = Blueprint('ExpeditionsAsync', url_prefix='asynchronous/expeditions')

def _init_repo(db_manager, tracer):
    repo = Repository(default=ExpeditionsRepositoryPSQL(db_manager, tracer), **{
        'expedition': ExpeditionsRepositoryPSQL(db_manager, tracer),
        'area': AreaRepositoryPSQL(db_manager, tracer),
        'plankton': PlanktonV4RepositoryAsync(tracer),
    })

    return repo

@bp_expeditions_async.route('/', methods=['GET'])
async def index(request):
    request_dict = RequestSanicDict(request)
    validator = JSONSchemaValidator()

    adict = request_dict.query_to_dict()
    adict = validator.get_default_param(adict)

    repo_init = _init_repo(db_manager=request.app.db, tracer=request.app.tracer)
    use_cases = ListExpeditionUsecase(repo=repo_init)
    request_object = ListAreaRequestObject.from_dict(adict, validator=validator)
    response_object = await use_cases.execute(request_object)

    print("**************ASYNC****************")
    print(response_object.type)
    print(response_object.value['message'])
    print("**************ASYNC****************")
    return json(response_object.value, status=Config.STATUS_CODES[response_object.type])