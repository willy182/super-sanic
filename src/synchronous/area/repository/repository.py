from abc import ABC, abstractmethod


class AreaRepository(ABC,object): #pragma: no cover

    @abstractmethod
    def get_all_area(self, request_objects): pass

    @abstractmethod
    def get_total_area(self, request_objects): pass

    @abstractmethod
    def get_subdistrict_by_zipcode(self, zipcode): pass