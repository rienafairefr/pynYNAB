import unittest
import uuid
import re

from pynYNAB.schema.Entity import Entity


id0 = '619a0ea1-11e8-4f10-8b9f-096b6158b315'
uuid0 = uuid.UUID(id0)
strings = [id0+'-2017-_07_09','mcb/test/'+id0,'mcb/'+id0,id0,id0+'/tttt']

class TestIdsCases(unittest.TestCase):
    def do_test(self, x, test_name):
        self.assertEqual(Entity.uuid_from_api(x), uuid0, msg=test_name)

    def test_ids(self):
        pass
        # Test some other functionality here

        for s in strings:
            test_name = 'test_%s' % re.sub('[^a-zA-Z0-9]+', '', s)
            self.do_test(s, test_name)

