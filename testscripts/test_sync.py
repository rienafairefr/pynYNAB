from pynYNAB.Client import clientfromargs
from pynYNAB.scripts.config import parser

print('test_live')
args = parser.parse_known_args()[0]
client = clientfromargs(args)
client.sync()
print('OK')
