import json
import re
from datetime import datetime

from aenum import Enum
from sqlalchemy import String, types, Date, DateTime, Enum as sqlaEnum
from sqlalchemy import TypeDecorator


class ArrayType(TypeDecorator):
    """ Sqlite-like does not support arrays.
        Let's use a custom type decorator.

        See http://docs.sqlalchemy.org/en/latest/core/types.html#sqlalchemy.types.TypeDecorator
    """
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self, **kw):
        return ArrayType(self.impl.length)


class AmountType(types.TypeDecorator):
    impl = types.Integer

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.Integer)

    def process_bind_param(self, value, dialect):
        return int(value * 1000) if value is not None else None

    def process_result_value(self, value, dialect):
        return float(value) / 1000 if value is not None else None


toapi_conversion_functions_table = {
    Date: lambda t, x: x.strftime('%Y-%m-%d'),
    DateTime: lambda t, x: x.strftime('%Y-%m-%dT%H:%M:%S.%f'),
    AmountType: lambda t, x: int(float(x) * 1000),
    sqlaEnum: lambda t, x: x._name_
}


def enumconversion(t, x):
    try:
        return t.enum_class[x]
    except KeyError:
        # received an invalid enum value
        return None


def date_from_api(columntype, string):
    result = re_date.search(string)
    if result is not None:
        return datetime.strptime(result.group(0), '%Y-%m-%d').date()


fromapi_conversion_functions_table = {
    Date: date_from_api,
    DateTime: lambda t, x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'),
    AmountType: lambda t, x: float(x) / 1000,
    sqlaEnum: enumconversion
}
re_uuid = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
re_date = re.compile(r'\d{4}[\/ .-]\d{2}[\/.-]\d{2}')


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


def flag(s):
    return 'ynab-flag-' + s


class ColorFlagType(Enum):
    Red = flag('red')
    Orange = flag('orange')
    Yellow = flag('yellow')
    Green = flag('green')
    Blue = flag('blue')
    Purple = flag('purple')


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