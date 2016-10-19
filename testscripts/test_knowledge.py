from pynYNAB.Client import clientfromargs
from pynYNAB.scripts.config import parser

# used to ping the nYNAB API to check that the sync works

args = parser.parse_known_args()[0]
client = clientfromargs(args)
client.sync()