from abc import ABCMeta, abstractmethod

class Validator(object):#pragma: no cover
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_valid(self, adict, schema, messages, draft): pass

    @abstractmethod
    def get_errors(self): pass

    @abstractmethod
    def get_valid_data(self): pass

    @abstractmethod
    def get_default_param(self, adict): pass
