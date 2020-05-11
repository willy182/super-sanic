from abc import ABC, abstractmethod


class ExpeditionsRepository(ABC,object): #pragma: no cover

    @abstractmethod
    async def get_all(self, filters): pass

    @abstractmethod
    async def get_by_id(self, id): pass
