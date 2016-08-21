import configargparse

from pynYNAB.Client import clientfromargs
from pynYNAB.Entity import UnknowEntityFieldValueError

parser = configargparse.getArgumentParser('pynYNAB')
args = parser.parse_known_args()[0]

try:
    client = clientfromargs(args)
    client.sync()
except UnknowEntityFieldValueError,e:
    print(e.message)
