from marshmallow import Schema, fields


class ExpeditionBaseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Str()
    name = fields.Str()
    code = fields.Str()
    availableFor = fields.Str(attribute="available_for", default='-')
