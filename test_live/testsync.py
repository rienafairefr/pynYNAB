import unittest

from pynYNAB.Client import clientfromargs
from pynYNAB.scripts.config import parser, get_logger

# sets up the logger
logger = get_logger()


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
