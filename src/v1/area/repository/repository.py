from abc import ABC, abstractmethod


class AreaRepository(ABC,object): #pragma: no cover

    @abstractmethod
    async def get_all_area(self, request_objects): pass

    @abstractmethod
    async def get_total_area(self, request_objects): pass

    @abstractmethod
    async def get_subdistrict_by_zipcode(self, zipcode): pass

    def db(self, t='read'):
        return self._db.get(t)