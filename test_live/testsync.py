import unittest

from pynYNAB.ClientFactory import clientfromargs
from pynYNAB.__main__ import parser


# used to ping the nYNAB API to check that the sync works
class TestSync(unittest.TestCase):
    @staticmethod
    def test_sync():
        print('test_live')
        args = parser.parse_known_args()[0]
        client = clientfromargs(args)
        client.sync()


if __name__ == '__main__':
    TestSync.test_sync()
