import datetime
import unittest

from sqlalchemy import Date

from pynYNAB.schema.Entity import fromapi_conversion_functions_table,toapi_conversion_functions_table
from pynYNAB.schema.types import AmountType


class TestConversionFunctions(unittest.TestCase):
    def doassert(self, t, v):
        toapi = toapi_conversion_functions_table[t]
        fromapi = fromapi_conversion_functions_table[t]
        converted_value = toapi(t,v)
        converted_back = fromapi(t,converted_value)
        self.assertEqual(v, converted_back)

    def test_scaling(self):
        value = 12.34
        self.doassert(AmountType,value)

    def test_date(self):
        value = datetime.date(2015,1,25)
        self.doassert(Date, value)

