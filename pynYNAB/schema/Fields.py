from pynYNAB.Entity import ListofEntities


class EntityField(object):
    def pretreat(self, x):
        return x

    def posttreat(self, x):
        return x

    def __init__(self, default):
        self.default = default

    def __call__(self, *args, **kwargs):
        return self.default


class EntityListField(object):
    def pretreat(self, x):
        return x

    def posttreat(self, x):
        return x

    def __init__(self, type):
        self.type = type

    def __call__(self, *args, **kwargs):
        return ListofEntities(self.type)