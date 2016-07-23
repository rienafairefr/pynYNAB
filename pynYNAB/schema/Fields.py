from datetime import datetime




class EntityField(object):
    def pretreat(self, x):
        return x

    def posttreat(self, x):
        return x

    def __init__(self, default):
        self.default=default

    def __call__(self, *args, **kwargs):
        if callable(self.default):
            return self.default()
        else:
            return self.default


class EntityListField(object):
    def pretreat(self, x):
        return x

    def posttreat(self, x):
        return x

    def __init__(self, typearg):
        self.type = typearg

    def __call__(self, *args, **kwargs):
        from pynYNAB.Entity import ListofEntities
        return ListofEntities(self.type)


class AmountField(EntityField):
    def __init__(self):
        super(AmountField, self).__init__(0)

    def pretreat(self, x):
        return int(x * 1000) if x is not None else x

    def posttreat(self, x):
        return float(x) / 1000 if x is not None else x


class PropertyField(EntityField):
    def __init__(self, lambdafun):
        self.lambdafun = lambdafun

    def __call__(self, *args, **kwargs):
        return self.lambdafun

class DateField(EntityField):
    def pretreat(self, x):
        return x.strftime('%Y-%m-%d') if x is not None else x

    def posttreat(self, x):
        try:
            return datetime.strptime(x, '%Y-%m-%d').date() if x is not None else x
        except ValueError:
            pass


class DatesField(EntityField):
    d = DateField(None)

    def hash(self,value):
        return hash(frozenset(value))

    def pretreat(self, x):
        try:
            return [self.d.pretreat(i) for i in x]
        except AttributeError:
            from pynYNAB.Entity import AccountTypes
            if x in AccountTypes:
                return x

    def posttreat(self, x):
        try:
            return [self.d.posttreat(i) for i in x]
        except:
            # nYNAB servers can accept an account with account_type not set to a valid value apparently
            return None

class AccountTypeField(EntityField):
    def pretreat(self, x):
        try:
            return x.name
        except AttributeError:
            from pynYNAB.Entity import AccountTypes
            if x in AccountTypes:
                return x

    def posttreat(self, x):
        from pynYNAB.Entity import AccountTypes
        try:
            return getattr(AccountTypes, x)
        except:
            # nYNAB servers can accept an account with account_type not set to a valid value apparently
            return None
