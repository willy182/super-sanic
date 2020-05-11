from sqlalchemy import select

from src.v1.area.repository.repository import AreaRepository
from src.v1.model.area import subdistrict_zipcode, subdistrict


class AreaRepositoryPSQL(AreaRepository):
    def __init__(self, db):
        self._db = db
        super(AreaRepositoryPSQL, self).__init__()

    async def get_subdistrict_by_zipcode(self, zipcode):
        query = select([subdistrict.c.name]).select_from(subdistrict.join(subdistrict_zipcode)) \
            .where(subdistrict_zipcode.c.zip_code == zipcode)
        try:
            data = await self.db('read').fetch_all(query)
        except Exception as e:
            data = e

        return data