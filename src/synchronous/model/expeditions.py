

class Expedition(object):
    def __init__(self, id, name, code, available_for, sub_district):
        self.id = id
        self.name = name
        self.code = code
        self.available_for = available_for
        self.sub_district = sub_district

    @classmethod
    def from_dict(cls, adict):
        expedition = Expedition(
            id=adict['id'],
            name=adict['name'],
            code=adict['code'],
            available_for=adict['available_for'],
            sub_district=SubDistrict.from_dict(adict['sub_district']),
        )

        return expedition


class SubDistrict(object):
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_dict(cls, adict):
        sub_district = Expedition(
            name=adict['name'],
        )

        return sub_district
