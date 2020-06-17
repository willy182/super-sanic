

class AllArea(object):
    def __init__(self, province, city, district, sub_district, zip_code):
        self.province = province
        self.city = city
        self.district = district
        self.sub_district = sub_district
        self.zip_code = zip_code

    @classmethod
    def from_dict(cls, adict):

        area = AllArea(
            province=adict['province'],
            city=adict['city'],
            district=adict['district'],
            sub_district=adict['sub_district'],
            zip_code=adict['zip_code'],
        )

        return area
