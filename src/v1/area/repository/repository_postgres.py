import time

from datetime import datetime
from sqlalchemy import select, func, or_, asc

from helpers.helper import get_result_subtraction_time
from src.v1.area.repository.repository import AreaRepository
from src.v1.model.area import subdistrict_zipcode, subdistrict, district, city, province


class AreaRepositoryPSQL(AreaRepository):
    def __init__(self, db, tracer):
        self._db = db
        self._tracer = tracer
        super(AreaRepositoryPSQL, self).__init__()

    async def get_all_area(self, request_objects):
        now1 = datetime.now()
        tt1 = now1.time()
        print('get_all_area_start', tt1)

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

        with self._tracer.start_span('start_get_all_area') as span:
            try:
                data = await self.db().fetch_all(query)

                now2 = datetime.now()
                tt2 = now2.time()
                print('get_all_area_end', tt2)
                str_time = get_result_subtraction_time(tt1, tt2)

                span.log_kv({'process_time': str_time})
                span.set_tag('query', query)
                span.set_tag('param', request_objects)
            except Exception as e:
                span.set_tag('error', e)
                data = e

        return data

    async def get_total_area(self, request_objects):
        now1 = datetime.now()
        tt1 = now1.time()
        print('get_total_area_start', tt1)

        query = select([func.count(province.c.name)]). \
            select_from(subdistrict_zipcode.join(subdistrict).
                        join(district).
                        join(city).
                        join(province))
        query = self._filter(query, request_objects)

        with self._tracer.start_span('start_get_total_area') as span:
            try:
                data = await self.db().execute(query)

                now2 = datetime.now()
                tt2 = now2.time()
                print('get_total_area_end', tt2)
                str_time = get_result_subtraction_time(tt1, tt2)

                span.log_kv({'process_time': str_time})
                span.set_tag('query', query)
                span.set_tag('param', request_objects)
            except Exception as e:
                span.set_tag('error', e)
                data = e

        return data

    async def get_subdistrict_by_zipcode(self, zipcode):
        now1 = datetime.now()
        tt1 = now1.time()
        print('get_subdistrict_by_zipcode_start', tt1)

        query = select([subdistrict.c.name]).select_from(subdistrict.join(subdistrict_zipcode)) \
            .where(subdistrict_zipcode.c.zip_code == zipcode)

        with self._tracer.start_span('start_get_subdistrict_by_zipcode') as span:
            try:
                data = await self.db().fetch_all(query)

                now2 = datetime.now()
                tt2 = now2.time()
                print('get_subdistrict_by_zipcode_end', tt2)
                str_time = get_result_subtraction_time(tt1, tt2)

                span.log_kv({'process_time': str_time})
                span.set_tag('query', query)
                span.set_tag('zipcode', zipcode)
            except Exception as e:
                span.set_tag('error', e)
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