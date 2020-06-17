from sanic import Blueprint
from sanic.response import json

from configs.config import Config
from helpers.validator.validator_jsonschema import JSONSchemaValidator
from src.shared.repository import Repository
from src.shared.request.request_sanic import RequestSanicDict
from src.asynchronous.area.repository.repository_postgres import AreaRepositoryPSQL
from src.asynchronous.area.usecase.request_object_area import ListAllAreaRequestObject
from src.asynchronous.area.usecase.usecase_area import ListAllAreaUsecase
from third_party.product.plankton import PlanktonV4RepositoryAsync

bp_area_async = Blueprint('AreaAsync', url_prefix='asynchronous/area')

def _init_repo(db_manager, tracer, session):
    repo = Repository(default=AreaRepositoryPSQL(db_manager, tracer), **{
        'area': AreaRepositoryPSQL(db_manager, tracer),
        'plankton': PlanktonV4RepositoryAsync(tracer, session),
    })

    return repo

@bp_area_async.route('/', methods=['GET'])
async def index(request):
    request_dict = RequestSanicDict(request)
    validator = JSONSchemaValidator()

    adict = request_dict.query_to_dict()
    adict = validator.get_default_param(adict)

    repo_init = _init_repo(db_manager=request.app.db, tracer=request.app.tracer, session=request.app.aiohttp_session)
    use_cases = ListAllAreaUsecase(repo=repo_init)
    request_object = ListAllAreaRequestObject.from_dict(adict, validator=validator)
    response_object = await use_cases.execute(request_object)

    print("==============ASYNC===============")
    print(response_object.type)
    print(response_object.value['message'])
    print("==============ASYNC===============")
    return json(response_object.value, status=Config.STATUS_CODES[response_object.type])