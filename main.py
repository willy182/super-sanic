from opentracing_instrumentation.client_hooks import install_all_patches
from jaeger_client import Config as JaegerConfig
from environs import Env
from sanic import Sanic
from tracer import SanicTracing

from configs.config_env import ConfigEnv
from configs.setup_db import connect_db, connect_db_simple
from middleware.middleware import setup_middlewares
from schemas.json.loader import JSONSchemaLoader
from src.v1.expeditions.delivery.http_handler import bp_expeditions_v1

app = Sanic(__name__)

env = Env()
env.read_env()

@app.listener('before_server_start')
async def connect_to_db(app, loop):
    app.db = connect_db(env)
    # app.db = connect_db_simple(env)

    # await app.db.connect()
    await app.db.get("read").connect()
    await app.db.get("write").connect()

@app.listener('before_server_start')
def setup_schemas(app, loop):
    """
    setup schema data
    :param app: application instance
    :param loop:
    :return:
    """
    JSONSchemaLoader.load(path='schemas/json/', filename="*.json")

@app.listener('after_server_stop')
async def disconnect_from_db(app):
    # await app.db.disconnect()
    await app.db.get("read").disconnect()
    await app.db.get("write").disconnect()

def initialize_tracer():
    install_all_patches()

    jaeger_config = JaegerConfig(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            'local_agent': {
                'reporting_host': ConfigEnv.JAEGER_HOST,
                'reporting_port': ConfigEnv.JAEGER_PORT,
            }
        },
        service_name=ConfigEnv.JAEGER_SERVICE_NAME,
    )

    return jaeger_config.initialize_tracer()

if __name__ == '__main__':
    tracer = initialize_tracer()
    sanic_tracing = SanicTracing(tracer, trace_all_requests=True, app=app)
    app.config.from_object(ConfigEnv)
    app.blueprint(bp_expeditions_v1)
    setup_middlewares(app)
    app.run(host=app.config.HOST, port=app.config.PORT, debug=app.config.DEBUG, auto_reload=app.config.DEBUG, workers=2)