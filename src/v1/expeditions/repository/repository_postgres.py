from sqlalchemy import select, func

from src.v1.expeditions.repository.repository import ExpeditionsRepository
from src.v1.model.expeditions import expeditions


class ExpeditionsRepositoryPSQL(ExpeditionsRepository):
    def __init__(self, db):
        self._db = db
        super(ExpeditionsRepositoryPSQL, self).__init__()

    async def get_all(self, filters):
        query = select([expeditions]).limit(10).offset(0)
        try:
            data = await self.db().fetch_all(query)
        except Exception as e:
            data = e

        return data

    async def get_total(self, filters):
        query = select([func.count()]).select_from(expeditions)
        try:
            data = await self.db().execute(query)
        except Exception as e:
            print(e, "error ")
            data = e

        return data

    async def get_by_id(self, id):
        query = expeditions.select().where('id' == id)
        try:
            data = await self.db().fetch_one(query)
        except Exception as e:
            data = e

        return data