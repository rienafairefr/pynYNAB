class BudgetNotFound(Exception):
    pass


class WrongPushException(Exception):
    def __init__(self, expected_delta, delta):
        self.expected_delta = expected_delta
        self.delta = delta

    string = 'tried to push a changed_entities with %d entities while we expected %d entities'

    @property
    def msg(self):
        return self.string % (self.delta, self.expected_delta)

    def __repr__(self):
        return self.msg


class NoBudgetNameException(ValueError):
    def __init__(self):
        super(NoBudgetNameException,self).__init__('you should pass a budget_name ')