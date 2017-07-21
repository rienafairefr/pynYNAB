import json
import logging
import re
from datetime import datetime

from aenum import Enum
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.base import ONETOMANY, MANYTOMANY
from sqlalchemy.sql.sqltypes import Enum as sqlaEnum, String, DateTime

from pynYNAB import KeyGenerator
from pynYNAB.schema.types import AmountType

LOG = logging.getLogger(__name__)

class AccountTypes(Enum):
    undef = 'undef'
    Checking = 'Checking'
    Savings = 'Savings'
    CreditCard = 'CreditCard'
    Cash = 'Cash'
    LineOfCredit = 'LineOfCredit'
    PayPal = 'PayPal'
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
            return obj.get_apidict()
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return json.JSONEncoder.default(self, obj)


class UnknowEntityFieldValueError(Exception):
    pass


class BaseModel(object):
    id = Column(String, primary_key=True, default=KeyGenerator.generateuuid)
    is_tombstone = Column(Boolean, default=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @property
    def listfields(self):
        relations = inspect(self.__class__).relationships
        return {k: relations[k].mapper.class_ for k in relations.keys() if
                relations[k].direction == ONETOMANY or relations[k].direction == MANYTOMANY}

    @property
    def scalarfields(self):
        scalarcolumns = self.__table__.columns
        return {k: scalarcolumns[k].type.__class__ for k in scalarcolumns.keys() if k != 'parent_id' and k != 'knowledge_id'}



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


def default_listener(col_attr, default):
    """Establish a default-setting listener.

    Given a class_, attrname, and a :class:`.DefaultGenerator` instance.
    The default generator should be a :class:`.ColumnDefault` object with a
    plain Python value or callable default; otherwise, the appropriate behavior
    for SQL functions and defaults should be determined here by the
    user integrating this feature.

    """

    @event.listens_for(col_attr, "init_scalar", retval=True, propagate=True)
    def init_scalar(target, value, dict_):

        if default.is_callable:
            # the callable of ColumnDefault always accepts a context
            # argument; we can pass it as None here.
            value = default.arg(None)
        elif default.is_scalar:
            value = default.arg
        else:
            # default is a Sequence, a SQL expression, server
            # side default generator, or other non-Python-evaluable
            # object.  The feature here can't easily support this.   This
            # can be made to return None, rather than raising,
            # or can procure a connection from an Engine
            # or Session and actually run the SQL, if desired.
            raise NotImplementedError(
                "Can't invoke pre-default for a SQL-level column default")

        # set the value in the given dict_; this won't emit any further
        # attribute set events or create attribute "history", but the value
        # will be used in the INSERT statement
        dict_[col_attr.key] = value

        # return the value as well
        return value


re_uuid = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
re_date = re.compile(r'\d{4}[\/ .-]\d{2}[\/.-]\d{2}')



def date_from_api(columntype, string):
    result = re_date.search(string)
    if result is not None:
        return datetime.strptime(result.group(0), '%Y-%m-%d').date()


fromapi_conversion_functions_table = {
    Date: date_from_api,
    DateTime: lambda t,x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'),
    AmountType: lambda t, x: float(x) / 1000,
    sqlaEnum: lambda t, x: t.enum_class[x]
}

toapi_conversion_functions_table = {
    Date: lambda t, x: x.strftime('%Y-%m-%d'),
    DateTime: lambda t, x: x.strftime('%Y-%m-%dT%H:%M:%S.%f'),
    AmountType: lambda t, x: int(float(x) * 1000),
    sqlaEnum: lambda t, x: x._name_
}


class Entity(BaseModel):
    def get_apidict(self):
        entityDict = self.get_dict()
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
        return (type(self), self.id).__str__()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        try:
            return self.key() == other.key()
        except:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def key(self,excludes=None):
        t = tuple()
        for k, v in self.get_dict().items():
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
        return cls.from_dict(cls.apidict_toinsertdict(entityDict))

    @classmethod
    def apidict_toinsertdict(cls, entityDict):
        modified_dict = {}
        for column in cls.__table__.columns:
            if column.name in entityDict and entityDict[column.name] is not None:
                conversion_function = fromapi_conversion_functions_table.get(column.type.__class__, lambda t, x: x)
                modified_dict[column.name] = conversion_function(column.type, entityDict[column.name])
        return modified_dict


Base = declarative_base(cls=Entity)

event.listen(BaseModel, 'mapper_configured', configure_listener, propagate=True)


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """

    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])


