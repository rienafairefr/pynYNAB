import logging
from dotenv import load_dotenv, find_dotenv

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.schema import Transaction
from pynYNAB.scripts.__main__ import parser

load_dotenv(find_dotenv())

print('test_sync')
args = parser.parse_known_args()[0]

LOG = logging.getLogger('pynYNAB.connection')
LOG.setLevel(logging.DEBUG)

client = nYnabClientFactory().create_client(args)
client.sync()
