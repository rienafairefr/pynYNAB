import datetime

from sqlalchemy import Date

from pynYNAB.schema import toapi_conversion_functions_table, fromapi_conversion_functions_table
from pynYNAB.schema.types import AmountType


def doassert(t, v):
    toapi = toapi_conversion_functions_table[t]
    fromapi = fromapi_conversion_functions_table[t]
    converted_value = toapi(t, v)
    converted_back = fromapi(t, converted_value)
    assert v == converted_back


def test_scaling():
    value = 12.34
    doassert(AmountType, value)


def test_date():
    value = datetime.date(2015, 1, 25)
    doassert(Date, value)
