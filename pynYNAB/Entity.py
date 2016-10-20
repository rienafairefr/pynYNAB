import copy
import json
import logging

from aenum import Enum

from pynYNAB import KeyGenerator
from pynYNAB.schema.Fields import EntityField, EntityListField, PropertyField

logger = logging.getLogger('pynYNAB')

def undef():
    pass


class AccountTypes(Enum):
    undef = 'undef'
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


on_budget_dict = dict(
    undef=None,
    Checking=True,
    Savings=True,
    CreditCard=True,
    Cash=True,
    LineOfCredit=True,
    Paypal=True,
    MerchantAccount=True,
    InvestmentAccount=False,
    Mortgage=False,
    OtherAsset=False,
    OtherLiability=False,
)
on_budget_dict[None] = None


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            pretreated = {}
            for namefield, field in obj.AllFields.items():
                value = getattr(obj, namefield)
                if value != undef:
                    pretreated[namefield] = field.pretreat(value)
            return pretreated
        elif isinstance(obj, ListofEntities):
            return list(obj)
        elif obj == undef:
            return
        else:
            return json.JSONEncoder.default(self, obj)


class UnknowEntityFieldValueError(Exception):
    pass


def obj_from_dict(obj_type, dictionary):
    treated = {}
    obt = obj_type()
    for key, value in dictionary.items():
        try:
            field = obt.AllFields[key]
        except KeyError:
            msg = 'Encountered field %s in a dictionary to create an entity of type %s, value %s ' % (key, obj_type,dictionary[key])
            logger.error(msg)
            raise UnknowEntityFieldValueError(msg)
        if isinstance(field, EntityField):
            treated[key] = field.posttreat(value)

    return obj_type(**treated)


ignored_fields_for_hash = ['id', 'credit_amount', 'cash_amount', 'feature_flags']


# adapted from http://stackoverflow.com/a/2954373/1685379
def addprop(inst, name, method, setter=None, cleaner=None):
    cls = type(inst)
    if not hasattr(cls, '__perinstance'):
        cls = type(cls.__name__, (cls,), {})
        cls.__perinstance = True
        inst.__class__ = cls
    p = property(method)
    setattr(cls, name, p)
    if setter is not None:
        setattr(cls, name, p.setter(setter))
    if cleaner is not None:
        setattr(cls, 'clean_' + name, cleaner)
    return p


class Entity(object):
    def __init__(self, *args, **kwargs):
        self.ListFields = {}
        self.Fields = {}
        self.AllFields = {}

        for namefield in dir(self):
            if namefield.startswith('__'): continue
            field = getattr(self, namefield)
            if isinstance(field, PropertyField):
                fieldc = copy.deepcopy(field)

                def getter(selfi):
                    if hasattr(selfi, '__prop_' + namefield):
                        return getattr(selfi, '__prop_' + namefield)
                    else:
                        return fieldc()(selfi)

                def setter(selfi, valuei):
                    setattr(selfi, '__prop_' + namefield, valuei)

                def cleaner(selfi):
                    delattr(selfi, '__prop_' + namefield)

                p = addprop(self, namefield, getter, setter, cleaner)
                if kwargs.get(namefield):
                    setattr(self.__class__, namefield, kwargs.get(namefield))
            elif isinstance(field, EntityField):
                self.Fields[namefield] = field
            elif isinstance(field, EntityListField):
                self.ListFields[namefield] = field
            else:
                continue
            self.AllFields[namefield] = field
            if isinstance(field, PropertyField): continue
            value = kwargs.get(namefield) if kwargs.get(namefield) is not None else field()
            setattr(self, namefield, value)
        super(Entity, self).__init__()

    id = EntityField(KeyGenerator.generateuuid)

    def __hash__(self):
        return self._hash()

    def _hash(self):
        t = tuple((k, v) for k, v in self.getdict().items() if k not in ignored_fields_for_hash)
        try:
            return hash(frozenset(t))
        except TypeError:
            pass

    def __str__(self):
        return self.getdict().__str__()

    def __repr__(self):
        return self.getdict().__repr__()

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


class ListofEntities(list):
    def __init__(self, typ):
        super(ListofEntities, self).__init__()
        from collections import OrderedDict
        self._dict_entities = OrderedDict()
        self._dict_entities_hash = {}
        self.typeItems = typ
        self.type_instance = typ()
        self.changed = []

    def _update_hashes(self):
        self._dict_entities_hash = {hash(v): v for k, v in self._dict_entities.items()}

    def __hash__(self):
        return hash(frozenset(self._dict_entities))

    def __str__(self):
        return self._dict_entities.__str__()

    def __repr__(self):
        return self._dict_entities.__repr__()

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
            self._dict_entities_hash[hash(o)] = o
        if track:
            self.changed.extend(objects)

    def append(self, o, track=True):
        if not isinstance(o, self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        self._dict_entities[o.id] = o
        self._dict_entities_hash[hash(o)] = o
        if track:
            self.changed.append(o)

    def delete(self, o, track=True):
        if not isinstance(o, self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        if o.id in self._dict_entities:
            del self._dict_entities[o.id]
        if hash(o) in self._dict_entities_hash:
            del self._dict_entities_hash[hash(o)]
        if track:
            o.is_tombstone = True
            self.changed.append(o)

    def modify(self, o, track=True):
        if not isinstance(o, self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        if o.id in self._dict_entities:
            h = hash(self._dict_entities[o.id])
            if h in self._dict_entities_hash:
                del self._dict_entities_hash[h]
            self._dict_entities[o.id] = o
            self._dict_entities_hash[hash(o)] = o
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
            return item._hash() in self._dict_entities_hash

    def __contains__(self, item):
        if not isinstance(item, self.typeItems):
            return False
        else:
            return item.id in self._dict_entities

    def get_changed_entities(self):
        return self.changed
