import unittest
import uuid
import re
from datetime import datetime

from pynYNAB.schema.Entity import date_from_api


strdate0 = '2015-04-03'
date0 = datetime.strptime(strdate0, '%Y-%m-%d').date()
datestrings = [strdate0+'T00:00:00',strdate0,'random+'+strdate0]


class TestDatesCases(unittest.TestCase):
    def do_test(self, x, test_name):
        self.assertEqual(date_from_api(None, x), date0, msg=test_name)

    def test_dates(self):
        pass
        # Test some other functionality here

        for s in datestrings:
            test_name = 'test_datefromapi_%s' % re.sub('[^a-zA-Z0-9]+', '', s)
            self.do_test(s, test_name)
