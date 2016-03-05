import json

from enum import Enum

import KeyGenerator
from config import logger


def undef():
    pass


AccountTypes = Enum('AccountType',names=('Checking', 'Savings', 'CreditCard', 'Cash', 'LineOfCredit', 'Paypal', 'MerchantAccount',
                    'InvestmentAccount', 'Mortgage', 'OtherAsset', 'OtherLiability'))


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            return {namefield: field.pretreat(getattr(obj, namefield)) for namefield, field in
                    obj.AllFields.iteritems()}
        elif isinstance(obj, ListofEntities):
            return obj._dict_entities.values()
        elif obj == undef:
            return
        else:
            return json.JSONEncoder.default(self, obj)


def obj_from_dict(obj_type, dictionary):
    treated = {}
    obt = obj_type()
    for key, value in dictionary.iteritems():
        try:
            field = obt.AllFields[key]
        except KeyError:
            logger.ERROR('Encountered field %s in a dictionary to create an entity of type %s ' % (key, obj_type))
            raise ValueError()
        if isinstance(field, EntityField):
            treated[key] = field.posttreat(value)

    return obj_type(**treated)


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


class Entity(object):
    def __init__(self, *args, **kwargs):
        for namefield in self.AllFields:
            value = kwargs.get(namefield) if kwargs.get(namefield) is not None else self.AllFields[namefield]()
            setattr(self, namefield, value)
        if self.id is None:
            self.id = self.create_id(*args, **kwargs)
        super(Entity, self).__init__()

    def __str__(self):
        return str(self.getdict())

    @property
    def AllFields(self):
        return dict(self.Fields.items() + self.CommonFields.items())

    CommonFields = dict(
        id=EntityField(None)
    )
    Fields = {}

    @property
    def ListFields(self):
        return {namefield: value for namefield, value in self.AllFields.iteritems() if
                isinstance(value, EntityListField)}

    def __unicode__(self):
        return self.__str__()

    def getdict(self):
        return {namefield: getattr(self, namefield) for namefield in self.AllFields}

    def get_changed_entities(self):
        firstrun = {namefield: getattr(self, namefield).get_changed_entities() for namefield in self.ListFields}
        return {namefield: value for namefield, value in firstrun.iteritems() if value != []}

    def update_from_changed_entities(self, changed_entities):
        for namefield in self.ListFields:
            getattr(self, namefield).update_from_changed_entities(changed_entities.get(namefield))

    def update_from_dict(self, d):
        self.__dict__.update(d)

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.getdict() == other.getdict()
        else:
            return False

    def create_id(self, *args, **kwargs):
        return KeyGenerator.generateUUID()


class ListofEntities(object):
    def __init__(self, typ):
        super(ListofEntities, self).__init__()
        from collections import OrderedDict
        self._dict_entities = OrderedDict()
        self.typeItems = typ
        self.type_instance = typ()
        self.changed = []

    def __str__(self):
        return self._dict_entities.values().__str__()

    def __unicode__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self._dict_entities.values().__getitem__(item)

    def update_from_changed_entities(self, changed_entities):
        if changed_entities is None:
            return
        for entity in changed_entities:
            try:
                self._dict_entities[entity.id].update_from_changed_entities(entity)
            except KeyError:
                self._dict_entities[entity.id] = entity

    def get(self, id):
        return self._dict_entities.get(id)

    def extend(self, objects, track=True):
        if not all(isinstance(x, self.typeItems) for x in objects):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        for o in objects:
            self._dict_entities[o.id] = o
        if track:
            self.changed.extend(objects)

    def append(self, o, track=True):
        if not isinstance(o, self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        self._dict_entities[o.id] = o
        if track:
            self.changed.append(o)

    def delete(self, o, track=True):
        if not isinstance(o, self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        if o.id in self._dict_entities:
            del self._dict_entities[o.id]
        if track:
            if not o.is_tombstone:
                o.is_tombstone = True
                self.changed.append(o)

    def modify(self, o, track=True):
        if not isinstance(o, self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        if o.id in self._dict_entities:
            self._dict_entities[o.id] = o
            if track:
                self.changed.append(o)

    def __iter__(self):
        return self._dict_entities.itervalues()

    def __len__(self):
        return len(self._dict_entities)

    def __contains__(self, item):
        if not isinstance(item, self.typeItems):
            return False
        else:
            return item.id in self._dict_entities

    def get_changed_entities(self):
        return self.changed
