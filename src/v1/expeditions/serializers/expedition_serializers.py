from marshmallow import Schema, fields


class ExpeditionBaseSchema(Schema):
    id = fields.Str(attribute="id", default="-")
    name = fields.Str(attribute="name", default='-')
    code = fields.Str(attribute="code", default='-')
    availableFor = fields.Str(attribute="available_for", default='-')
