from abc import ABCMeta, abstractmethod


class PlanktonRepository():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_variant(self, request): pass
