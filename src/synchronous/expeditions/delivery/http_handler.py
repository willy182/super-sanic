from sanic import Blueprint
from sanic.response import json

from configs.config import Config
from helpers.validator.validator_jsonschema import JSONSchemaValidator
from src.shared.repository import Repository
from src.shared.request.request_sanic import RequestSanicDict
from src.synchronous.area.repository.repository_postgres import AreaRepositoryPSQL
from src.synchronous.expeditions.repository.repository_postgres import ExpeditionsRepositoryPSQL
from src.synchronous.expeditions.usecase.request_object_expedtions import ListAreaRequestObject
from src.synchronous.expeditions.usecase.usecase_expeditions import ListExpeditionUsecase
from third_party.product.plankton import PlanktonV4RepositorySync

bp_expeditions_sync = Blueprint('ExpeditionsSync', url_prefix='synchronous/expeditions')

def _init_repo(db_manager):
    repo = Repository(default=ExpeditionsRepositoryPSQL(db_manager), **{
        'expedition': ExpeditionsRepositoryPSQL(db_manager),
        'area': AreaRepositoryPSQL(db_manager),
        'plankton': PlanktonV4RepositorySync(),
    })

    return repo

@bp_expeditions_sync.route('/', methods=['GET'])
async def index(request):
    request_dict = RequestSanicDict(request)
    validator = JSONSchemaValidator()

    adict = request_dict.query_to_dict()
    adict = validator.get_default_param(adict)

    repo_init = _init_repo(db_manager=request.app.db_orator)
    use_cases = ListExpeditionUsecase(repo=repo_init)
    request_object = ListAreaRequestObject.from_dict(adict, validator=validator)
    response_object = use_cases.execute(request_object)

    print("*************SYNC*******************")
    print(response_object.type)
    print(response_object.value['message'])
    print("*************SYNC***************")
    return json(response_object.value, status=Config.STATUS_CODES[response_object.type])