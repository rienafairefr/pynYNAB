import logging

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.base import ONETOMANY
from sqlalchemy.sql.sqltypes import String

from pynYNAB import KeyGenerator
from pynYNAB.schema.types import on_budget_dict, toapi_conversion_functions_table, fromapi_conversion_functions_table

LOG = logging.getLogger(__name__)

on_budget_dict[None] = None


def listfields(cls):
    relations = inspect(cls).relationships
    returnvalue = {k: relations[k].mapper.class_ for k in relations.keys() if
            relations[k].direction == ONETOMANY}
    return returnvalue


def scalarfields(cls):
    scalarcolumns = inspect(cls).columns
    returnvalue = {k: scalarcolumns[k].type.__class__ for k in scalarcolumns.keys() if
            k != 'parent_id' and k != 'knowledge_id'}
    return returnvalue


class BaseModel(object):
    id = Column(String, primary_key=True, default=KeyGenerator.generateuuid)
    is_tombstone = Column(Boolean, default=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __new__(cls, *args, **kwargs):
        new_obj = super(BaseModel, cls).__new__(cls)
        setattr(new_obj, 'listfields', listfields(cls))
        setattr(new_obj, 'scalarfields', scalarfields(cls))

        return new_obj

    def __init__(self):
        super(BaseModel, self).__init__(self)
        setattr(self, 'bin', self.__class__())


class Entity(BaseModel):
    def get_apidict(self):
        return self.dict_to_apidict(self.get_dict())

    @classmethod
    def dict_to_apidict(self, entityDict):
        for column in self.__table__.columns:
            if column.name in entityDict and entityDict[column.name] is not None:
                conversion_function = toapi_conversion_functions_table.get(column.type.__class__, lambda t, x: x)
                entityDict[column.name] = conversion_function(column.type, entityDict[column.name])
        return entityDict

    def get_dict(self):
        return {key: getattr(self, key) for key in self.scalarfields if key != 'parent_id'}

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return (type(self).__name__, self.id).__str__()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        try:
            return self.key() == other.key()
        except:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def key(self, excludes=None):
        t = tuple()
        for k, v in self.get_dict().items():
            if excludes and k in excludes:
                continue
            if isinstance(v, list):
                t += tuple(v)
            else:
                t += (v,)
        return t

    @classmethod
    def key_from_dict(cls, input_dict, excludes=None):
        t = tuple()
        for k, v in input_dict.items():
            if excludes and k in excludes:
                continue
            if isinstance(v, list):
                t += tuple(v)
            else:
                t += (v,)
        return t

    @property
    def key2(self):
        return self.key(excludes=['id'])

    def __hash__(self):
        return hash(self.key())

    def copy(self):
        returnvalue = type(self)(**self.get_dict())
        return returnvalue

    @classmethod
    def from_dict(cls, entitydict):
        return cls(**entitydict)

    @classmethod
    def from_apidict(cls, entityDict):
        return cls.from_dict(cls.apidict_todict(entityDict))

    @classmethod
    def apidict_todict(cls, entityDict):
        modified_dict = {}
        for column in cls.__table__.columns:
            if column.name in entityDict and entityDict[column.name] is not None:
                conversion_function = fromapi_conversion_functions_table.get(column.type.__class__, lambda t, x: x)
                modified_dict[column.name] = conversion_function(column.type, entityDict[column.name])
        return modified_dict


def configure_listener(mapper, class_):
    for col_attr in mapper.column_attrs:
        column = col_attr.columns[0]
        if column.default is not None:
            default_listener(col_attr, column.default)

    for rel_attr in mapper.relationships:
        expectedtype_listener(rel_attr)

def expectedtype_listener(rel_attr):
    @event.listens_for(rel_attr, 'append')
    def append(target, value, initiator):
        expected_type = initiator.parent_token.mapper.class_
        value_type = type(value)
        if expected_type != value_type:
            raise ValueError('type %s, attribute %s, expect a %s, received a %s ' % (
                type(target), rel_attr.key, expected_type, value_type))

    @event.listens_for(rel_attr, 'set')
    def set(target, value, oldvalue, initiator):
        expected_type = initiator.parent_token.mapper.class_
        value_type = type(value)
        if expected_type != value_type:
            raise ValueError('type %s, attribute %s, expect a %s, received a %s ' % (
                type(target), rel_attr.key, expected_type, value_type))

def default_listener(col_attr, default):
    """Establish a default-setting listener."""

    @event.listens_for(col_attr, "init_scalar", retval=True, propagate=True)
    def init_scalar(target, value, dict_):

        if default.is_callable:
            # the callable of ColumnDefault always accepts a context argument
            value = default.arg(None)
        elif default.is_scalar:
            value = default.arg
        else:
            raise NotImplementedError(
                "Can't invoke pre-default for a SQL-level column default")

        dict_[col_attr.key] = value

        return value


Base = declarative_base(cls=Entity)

event.listen(BaseModel, 'mapper_configured', configure_listener, propagate=True)
