class Repository(object):
    __default = None

    def __init__(self, default, **kwargs):
        self.__dict__ = default.__dict__

        for key in kwargs:
            setattr(self, key, kwargs.get(key))


class FactoryRepository(object):
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs.get(key))
