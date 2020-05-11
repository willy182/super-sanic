from src.v1.area.repository.repository import AreaRepository
from src.v1.model.area import subdistrict_zipcode, subdistrict


class AreaRepositoryPSQL(AreaRepository):
    def __init__(self, db):
        self.db = db
        super(AreaRepositoryPSQL, self).__init__()

    async def get_subdistrict_by_zipcode(self, zipcode):
        query = subdistrict_zipcode.join(subdistrict).select([subdistrict.c.name])\
            .where('zip_code' == zipcode)
        try:
            data = await self.db.fetch_all(query)
        except Exception as e:
            data = e

        return data