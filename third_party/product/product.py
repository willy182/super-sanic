from abc import ABCMeta, abstractmethod


class PlanktonRepository(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_variant(self, request): pass
