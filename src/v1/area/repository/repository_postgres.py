from sqlalchemy import select, func, or_, asc

from src.v1.area.repository.repository import AreaRepository
from src.v1.model.area import subdistrict_zipcode, subdistrict, district, city, province


class AreaRepositoryPSQL(AreaRepository):
    def __init__(self, db):
        self._db = db
        super(AreaRepositoryPSQL, self).__init__()

    async def get_all_area(self, request_objects):
        query = select([province.c.name.label('province'), city.c.name.label('city'), city.c.type,
                        district.c.name.label('district'), subdistrict.c.name.label('subdistrict'),
                        subdistrict_zipcode.c.zip_code]).\
            select_from(subdistrict_zipcode.join(subdistrict).
                        join(district).
                        join(city).
                        join(province))
        query = self._filter(query, request_objects)
        query = query.order_by(asc(province.c.name), asc(city.c.name)).\
                limit(request_objects.limit).offset(request_objects.offset)

        try:
            data = await self.db().fetch_all(query)
        except Exception as e:
            data = e

        return data

    async def get_total_subdistrict(self, request_objects):
        query = select([func.count(province.c.name)]). \
            select_from(subdistrict_zipcode.join(subdistrict).
                        join(district).
                        join(city).
                        join(province))

        query = self._filter(query, request_objects)

        try:
            data = await self.db().execute(query)
        except Exception as e:
            print(e, "error ")
            data = e

        return data

    async def get_subdistrict_by_zipcode(self, zipcode):
        query = select([subdistrict.c.name]).select_from(subdistrict.join(subdistrict_zipcode)) \
            .where(subdistrict_zipcode.c.zip_code == zipcode)
        try:
            data = await self.db().fetch_all(query)
        except Exception as e:
            data = e

        return data

    def _filter(self, query, request_objects):
        if request_objects.q != "":
            like = '%{}%'.format(request_objects.q.lower())
            query = query.where(or_(
                func.lower(province.c.name).like(like),
                func.lower(city.c.name).like(like),
                func.lower(district.c.name).like(like)
            ))

        return query