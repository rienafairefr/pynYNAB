import unittest
import uuid
import re
from datetime import datetime

from pynYNAB.schema.Entity import date_from_api, uuid_from_api

id0 = '619a0ea1-11e8-4f10-8b9f-096b6158b315'
uuid0 = uuid.UUID(id0)
idstrings = [id0+'-2017-_07_09','mcb/test/'+id0,'mcb/'+id0,id0,id0+'/tttt']


class TestIdsCases(unittest.TestCase):
    def do_test(self, x, test_name):
        self.assertEqual(uuid_from_api(None, x), uuid0, msg=test_name)

    def test_ids(self):
        pass
        # Test some other functionality here

        for s in idstrings:
            test_name = 'test_idfromapi_%s' % re.sub('[^a-zA-Z0-9]+', '', s)
            self.do_test(s, test_name)


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

