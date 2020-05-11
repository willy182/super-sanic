from abc import ABCMeta, abstractmethod

class Request(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def form_to_dict(): pass

    @abstractmethod
    def json_to_dict(): pass

    @abstractmethod
    def query_to_dict(): pass

    @abstractmethod
    def parse_all_to_dict(): pass