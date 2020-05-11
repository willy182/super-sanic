from sanic_envconfig import EnvConfig


class ConfigEnv(EnvConfig):
    DEBUG: bool = False
    HOST: str = ''
    PORT: int = 0
    DB_URL: str = ''
    PLANKTON_API_HOST: str = ''
    PLANKTON_API_ACCEPT: str = ''
    PLANKTON_API_BASIC_AUTH: str = ''
    JAEGER_HOST: str = ''
    JAEGER_PORT: str = ''
    JAEGER_SERVICE_NAME: str = ''
