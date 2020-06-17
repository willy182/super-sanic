from abc import ABC, abstractmethod


class ExpeditionsRepository(ABC,object): #pragma: no cover

    @abstractmethod
    def get_all(self, request_objects): pass

    @abstractmethod
    def get_total(self, request_objects): pass

    @abstractmethod
    def get_by_id(self, id): pass
