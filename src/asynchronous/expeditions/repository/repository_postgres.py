from datetime import datetime
from sqlalchemy import select, func

from helpers.helper import get_result_subtraction_time
from src.asynchronous.expeditions.repository.repository import ExpeditionsRepository
from src.asynchronous.model.expeditions import expeditions


class ExpeditionsRepositoryPSQL(ExpeditionsRepository):
    def __init__(self, db, tracer):
        self._db = db
        self._tracer = tracer
        super(ExpeditionsRepositoryPSQL, self).__init__()

    async def get_all(self, request_objects):
        now1 = datetime.now()
        tt1 = now1.time()
        # print('get_all_start', tt1)

        query = select([expeditions]).limit(10).offset(0)

        with self._tracer.start_span('start_get_all_expedition') as span:
            try:
                data = await self.db().fetch_all(query)

                now2 = datetime.now()
                tt2 = now2.time()
                # print('get_all_end', tt2)
                str_time = get_result_subtraction_time(tt1, tt2)

                span.log_kv({'process_time': str_time})
                span.set_tag('query', query)
                span.set_tag('param', request_objects)
            except Exception as e:
                span.set_tag('error', e)
                data = e

        return data

    async def get_total(self, request_objects):
        now1 = datetime.now()
        tt1 = now1.time()
        # print('get_total_start', tt1)

        query = select([func.count()]).select_from(expeditions)

        with self._tracer.start_span('start_get_total_expedition') as span:
            try:
                data = await self.db().execute(query)

                now2 = datetime.now()
                tt2 = now2.time()
                # print('get_total_end', tt2)
                str_time = get_result_subtraction_time(tt1, tt2)

                span.log_kv({'process_time': str_time})
                span.set_tag('query', query)
                span.set_tag('param', request_objects)
            except Exception as e:
                span.set_tag('error', e)
                data = e

        return data

    async def get_by_id(self, id):
        now1 = datetime.now()
        tt1 = now1.time()
        # print('get_by_id_start', tt1)

        query = expeditions.select().where(expeditions.c.id == id)

        with self._tracer.start_span('start_get_total_expedition') as span:
            try:
                data = await self.db().fetch_one(query)

                now2 = datetime.now()
                tt2 = now2.time()
                # print('get_by_id_end', tt2)
                str_time = get_result_subtraction_time(tt1, tt2)

                span.log_kv({'process_time': str_time})
                span.set_tag('query', query)
                span.set_tag('id', id)
            except Exception as e:
                span.set_tag('error', e)
                data = e

        return data