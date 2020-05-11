import os, glob, json


class JSONSchemaLoader(object):
    __json_schemas = {}

    def __init__(self):
        super(JSONSchemaLoader, self).__init__()

    @classmethod
    def load(cls, path, filename):
        for file in glob.glob(os.path.join(path, filename)):
            schema = json.loads(open(file, 'r').read())
            if isinstance(schema, list):
                for s in schema:
                    cls.__json_schemas[s['id']] = s
                continue

            cls.__json_schemas[schema['id']] = schema

    @classmethod
    def get(cls, schema_id):
        return cls.__json_schemas[schema_id]
