from sanic import Blueprint
from sanic.response import json

from configs.config import Config
from helpers.validator.validator_jsonschema import JSONSchemaValidator
from src.shared.repository import Repository
from src.shared.request.request_sanic import RequestSanicDict
from src.synchronous.area.repository.repository_postgres import AreaRepositoryPSQL
from src.synchronous.area.usecase.request_object_area import ListAllAreaRequestObject
from src.synchronous.area.usecase.usecase_area import ListAllAreaUsecase, ListAllOnlyAreaUsecase
from third_party.product.plankton import PlanktonV4RepositorySync

bp_area_sync = Blueprint('AreaSync', url_prefix='synchronous/area')

def _init_repo(db_manager):
    repo = Repository(default=AreaRepositoryPSQL(db_manager), **{
        'area': AreaRepositoryPSQL(db_manager),
        'plankton': PlanktonV4RepositorySync(),
    })

    return repo

@bp_area_sync.route('/', methods=['GET'])
async def index(request):
    request_dict = RequestSanicDict(request)
    validator = JSONSchemaValidator()

    adict = request_dict.query_to_dict()
    adict = validator.get_default_param(adict)

    repo_init = _init_repo(db_manager=request.app.db_orator)
    use_cases = ListAllAreaUsecase(repo=repo_init)
    request_object = ListAllAreaRequestObject.from_dict(adict, validator=validator)
    response_object = use_cases.execute(request_object)

    print("==============SYNC=================")
    print(response_object.type)
    print(response_object.value['message'])
    print("==============SYNC=================")
    return json(response_object.value, status=Config.STATUS_CODES[response_object.type])

@bp_area_sync.route('/only-database', methods=['GET'])
async def index(request):
    request_dict = RequestSanicDict(request)
    validator = JSONSchemaValidator()

    adict = request_dict.query_to_dict()
    adict = validator.get_default_param(adict)

    repo_init = _init_repo(db_manager=request.app.db_orator)
    use_cases = ListAllOnlyAreaUsecase(repo=repo_init)
    request_object = ListAllAreaRequestObject.from_dict(adict, validator=validator)
    response_object = use_cases.execute(request_object)

    print("==============SYNC=================")
    print(response_object.type)
    print(response_object.value['message'])
    print("==============SYNC=================")
    return json(response_object.value, status=Config.STATUS_CODES[response_object.type])