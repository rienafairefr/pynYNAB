import json

from enum import Enum

from pynYNAB import KeyGenerator
from pynYNAB.schema.Fields import EntityField, EntityListField
from pynYNAB.config import get_logger
from pynYNAB.utils import equal_dicts


def undef():
    pass


class AccountTypes(Enum):
    Checking = 'Checking'
    Savings = 'Savings'
    CreditCard = 'CreditCard'
    Cash = 'Cash'
    LineOfCredit = 'LineOfCredit'
    Paypal = 'Paypal'
    MerchantAccount = 'MerchantAccount'
    InvestmentAccount = 'InvestmentAccount'
    Mortgage = 'Mortgage'
    OtherAsset = 'OtherAsset'
    OtherLiability = 'OtherLiability'


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            pretreated={}
            for namefield, field in obj.AllFields.items():
                value=getattr(obj, namefield)
                if value != undef:
                    pretreated[namefield]=field.pretreat(value)
            return pretreated
        elif isinstance(obj, ListofEntities):
            return list(obj)
        elif obj == undef:
            return
        else:
            return json.JSONEncoder.default(self, obj)


def obj_from_dict(obj_type, dictionary):
    treated = {}
    obt = obj_type()
    for key, value in dictionary.items():
        try:
            field = obt.AllFields[key]
        except KeyError:
            get_logger().error('Encountered field %s in a dictionary to create an entity of type %s ' % (key, obj_type))
            raise ValueError()
        if isinstance(field, EntityField):
            treated[key] = field.posttreat(value)

    return obj_type(**treated)


ignored_fields_for_hash = ['id', 'credit_amount', 'cash_amount']


class Entity(object):
    def __init__(self, *args, **kwargs):
        for namefield in self.AllFields:
            value = kwargs.get(namefield) if kwargs.get(namefield) is not None else self.AllFields[namefield]()
            setattr(self, namefield, value)
        if self.id is None:
            self.id = self.create_id(*args, **kwargs)
        super(Entity, self).__init__()

    def hash(self):
        return hash(frozenset({k: v for k, v in self.getdict().items() if k not in ignored_fields_for_hash}.items()))

    def __str__(self):
        return str(self.getdict())

    @property
    def AllFields(self):
        return dict(list(self.Fields.items()) + list(self.CommonFields.items()))

    CommonFields = dict(
        id=EntityField(None)
    )
    Fields = {}

    @property
    def ListFields(self):
        return {namefield: value for namefield, value in self.AllFields.items() if
                isinstance(value, EntityListField)}

    def __unicode__(self):
        return self.__str__()

    def getdict(self):
        return {namefield: getattr(self, namefield) for namefield in self.AllFields}

    def get_changed_entities(self):
        firstrun = {namefield: getattr(self, namefield).get_changed_entities() for namefield in self.ListFields}
        return {namefield: value for namefield, value in firstrun.items() if value != []}

    def update_from_changed_entities(self, changed_entities):
        for namefield in self.ListFields:
            getattr(self, namefield).update_from_changed_entities(changed_entities.get(namefield))

    def update_from_dict(self, d):
        self.__dict__.update(d)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.getdict() == other.getdict()
        else:
            return False

    def create_id(self, *args, **kwargs):
        return KeyGenerator.generateuuid()


class ListofEntities(object):
    def __init__(self, typ):
        super(ListofEntities, self).__init__()
        from collections import OrderedDict
        self._dict_entities = OrderedDict()
        self._dict_entities_hash = {}
        self.typeItems = typ
        self.type_instance = typ()
        self.changed = []

    def _update_hashes(self):
        self._dict_entities_hash = {v.hash(): v for k, v in self._dict_entities.items()}

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
            if hasattr(entity, 'is_tombstone') and entity.is_tombstone:
                continue
            try:
                self._dict_entities[entity.id].update_from_changed_entities(entity)
            except KeyError:
                self._dict_entities[entity.id] = entity
        self._update_hashes()

    def get(self, entity_id):
        return self._dict_entities.get(entity_id)

    def extend(self, objects, track=True):
        if not all(isinstance(x, self.typeItems) for x in objects):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        for o in objects:
            self._dict_entities[o.id] = o
            self._dict_entities_hash[o.hash()] = o
        if track:
            self.changed.extend(objects)

    def append(self, o, track=True):
        if not isinstance(o, self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        self._dict_entities[o.id] = o
        self._dict_entities_hash[o.hash()] = o
        if track:
            self.changed.append(o)

    def delete(self, o, track=True):
        if not isinstance(o, self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        if o.id in self._dict_entities:
            del self._dict_entities[o.id]
            del self._dict_entities_hash[o.hash()]
        if track:
            o.is_tombstone = True
            self.changed.append(o)

    def modify(self, o, track=True):
        if not isinstance(o, self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        if o.id in self._dict_entities:
            del self._dict_entities_hash[self._dict_entities[o.id].hash()]
            self._dict_entities[o.id] = o
            self._dict_entities_hash[o.hash()] = o
            if track:
                self.changed.append(o)

    def __iter__(self):
        return self._dict_entities.values().__iter__()

    def __len__(self):
        return len(self._dict_entities)

    def containsduplicate(self, item):
        if not isinstance(item, self.typeItems):
            return False
        else:
            return item.hash() in self._dict_entities_hash

    def __contains__(self, item):
        if not isinstance(item, self.typeItems):
            return False
        else:
            return item.id in self._dict_entities

    def get_changed_entities(self):
        return self.changed
