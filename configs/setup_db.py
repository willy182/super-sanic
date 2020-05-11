from databases import Database


def config_db(env):
    config = {
        'default': 'read',
        'read': {
            'host': env("POSTGRE_HOST_READ"),
            'driver': 'postgresql',
            'database': env("POSTGRE_DATABASE"),
            'user': env("POSTGRE_USERNAME"),
            'password': env("POSTGRE_PASSWORD"),
            'prefix': '',
            'port': env("POSTGRE_PORT")
        },
        'write': {
            'host': env("POSTGRE_HOST_WRITE"),
            'driver': 'postgresql',
            'database': env("POSTGRE_DATABASE"),
            'user': env("POSTGRE_USERNAME"),
            'password': env("POSTGRE_PASSWORD"),
            'prefix': '',
            'port': env("POSTGRE_PORT")
        }
    }

    return config

def connect_db_simple(env):
    db_url = env("DB_URL")

    return Database(db_url)

def connect_db(env):
    config = config_db(env)

    db = DatabaseManager(config)

    connection = {
        "read": db.add("read"),
        "write": db.add("write"),
    }

    return connection


class DatabaseManager(object):
    def __init__(self, config):
        self.config = config
        self.db_store = None

    def add(self, conn_name):
        db_url = "{}://{}:{}@{}:{}/{}".format(self.config.get(conn_name).get("driver"),
                                              self.config.get(conn_name).get("user"),
                                              self.config.get(conn_name).get("password"),
                                              self.config.get(conn_name).get("host"),
                                              self.config.get(conn_name).get("port"),
                                              self.config.get(conn_name).get("database"))

        try:
            self.db_store = Database(db_url)
        except Exception as e:
            print(e)

        return self.db_store
