from marshmallow import Schema, fields


class AreaBaseSchema(Schema):
    name = fields.Str()


class AllAreaBaseSchema(Schema):
    class Meta:
        ordered = True

    province = fields.Str()
    city = fields.Str()
    district = fields.Str()
    subDistrict = fields.Str(attribute="subdistrict", default="-")
    zipCode = fields.Str(attribute="zip_code", default="-")
