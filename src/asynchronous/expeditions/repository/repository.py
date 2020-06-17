from abc import ABC, abstractmethod


class ExpeditionsRepository(ABC,object): #pragma: no cover

    @abstractmethod
    async def get_all(self, request_objects): pass

    @abstractmethod
    async def get_total(self, request_objects): pass

    @abstractmethod
    async def get_by_id(self, id): pass

    def db(self, t='read'):
        return self._db.get(t)
