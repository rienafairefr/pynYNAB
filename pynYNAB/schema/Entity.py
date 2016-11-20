import copy
import json
import logging
from uuid import UUID

import functools
from aenum import Enum
from sqlalchemy import Column
from sqlalchemy import event
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from pynYNAB import KeyGenerator
from pynYNAB.schema.Fields import EntityField, EntityListField, PropertyField
from pynYNAB.schema.types import NYNAB_GUID

logger = logging.getLogger('pynYNAB')
from sqlalchemy import inspect

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
            return obj.getdict()
        elif isinstance(obj,UUID):
            return str(obj)
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
            msg = 'Encountered field %s in a dictionary to create an entity of type %s, value %s ' % (
            key, obj_type, dictionary[key])
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


class BaseModel(object):
    id = Column(NYNAB_GUID, primary_key=True, default=KeyGenerator.generateuuid)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Changed(BaseModel):
    pass


class Entity(BaseModel):
    def getdict(self):
        return self.__dict__


changed = {}

class Root(BaseModel):
    @property
    def ListFields(self):
        relations = inspect(self.__class__).relationships
        return {k:relations[k].mapper.class_ for k in relations.keys()}

    @property
    def ScalarFields(self):
        scalarcolumns = self.__table__.columns
        return {k: scalarcolumns[k].type.__class__.__name__ for k in scalarcolumns.keys()}

    def get_changed_entities(self):
        return {key: value for key,value in self.changed.items() if value !=[]}

    def clear_changed_entities(self):
        self.__changed = {k: [] for k in self.ListFields}

    def getdict(self):
        objs_dict = {}
        for key in self.ListFields:
            objs_dict[key] = []
            for instance in getattr(self,key):
                objs_dict[key].append(instance.getdict())


def ensure_changed(instance,key):
    try:
        changed_list = changed[instance.id][key]
    except:
        changed[instance.id] = {}
        changed[instance.id] = {}
        changed[instance.id][key] = []
        changed_list = changed[instance.id][key]


def configure_entity_listener(class_, key, inst):
    def set_(instance, value, oldvalue, initiator):
        if not hasattr(instance,'parent'):
            return
        parent = instance.parent
        if parent is not None:
            for relationship in parent.__mapper__.relationships:
                if relationship.mapper == instance.__mapper__:

                    changed_list.append(instance)

    event.listen(inst, 'set', set_)


def configure_listener(class_, key, inst):
    def append(instance, value, initiator):
        if not instance.is_root:
            return
        if instance.changed is None:
            instance.changed = class_()
        entities_list = getattr(instance.changed, initiator.key)
        entities_list.append(value)

    def remove(instance, value, initiator):
        if not instance.is_root:
            return
        if instance.changed is None:
            instance.changed = class_()
        value.is_tombstone=True
        entities_list = getattr(instance.changed, initiator.key)
        entities_list.append(value)

    event.listen(inst, 'append', append)
    event.listen(inst, 'remove', remove)

    #for relationship in class_.__mapper__.relationships:
     #   remote_class = getattr(class_,relationship.key).class_
     #   event.listen(remote_class,'attribute_instrument',configure_entity_listener)

Base = declarative_base(cls=Entity)

event.listen(Root, 'attribute_instrument', configure_listener)
event.listen(Entity, 'attribute_instrument', configure_entity_listener)

class EntityCls(object):
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
