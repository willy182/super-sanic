from helpers.helper import get_value_from_dict
from src.synchronous.area.repository.repository import AreaRepository


class AreaRepositoryPSQL(AreaRepository):
    def __init__(self, db):
        self.db = db

        super(AreaRepositoryPSQL, self).__init__()

    def get_all_area(self, filters):
        query = self._filter(filters)
        query = query.order_by('bc_province.name', 'ASC')
        query = query.order_by('bc_city.name', 'ASC')
        query = query.offset(filters.offset).limit(filters.limit)

        return query.get()

    def get_total_area(self, filters):
        query = self._filter(filters)

        return query.count()

    def get_subdistrict_by_zipcode(self, zipcode):
        query = self.db.table('bc_subdistrict')
        query = query.join('bc_subdistrict_zipcode', 'bc_subdistrict.id', '=', 'bc_subdistrict_zipcode.subdistrict_id')
        query = query.select('bc_subdistrict.name')
        query = query.where('bc_subdistrict_zipcode.zip_code', '=', zipcode)

        return query.get()

    def _filter(self, filters):
        query = self.db.table('bc_subdistrict_zipcode')
        query = query.join('bc_subdistrict', 'bc_subdistrict_zipcode.subdistrict_id', '=', 'bc_subdistrict.id')
        query = query.join('bc_district', 'bc_subdistrict.district_id', '=', 'bc_district.id')
        query = query.join('bc_city', 'bc_district.city_id', '=', 'bc_city.id')
        query = query.join('bc_province', 'bc_city.province_id', '=', 'bc_province.id')
        query = query.select(
            'bc_province.name AS province', 'bc_city.name AS city', 'bc_city.type', 'bc_district.name AS district',
            'bc_subdistrict.name AS subdistrict', 'bc_subdistrict_zipcode.zip_code'
        )

        q = filters.q.lower()
        if filters.q != "":
            query = query.or_where(self.db.raw('LOWER(bc_province.name)'), 'like', '%{}%'.format(q))
            query = query.or_where(self.db.raw('LOWER(bc_city.name)'), 'like', '%{}%'.format(q))
            query = query.or_where(self.db.raw('LOWER(bc_district.name)'), 'like', '%{}%'.format(q))

        return query