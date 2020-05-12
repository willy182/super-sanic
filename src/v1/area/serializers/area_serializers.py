from marshmallow import Schema, fields


class AreaBaseSchema(Schema):
    name = fields.Str(attribute="name", default='-')
