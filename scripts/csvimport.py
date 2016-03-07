import configargparse

from pynYNAB.connection import nYnabConnection

parser = configargparse.getArgumentParser('pynYNAB')
parser.description='Manually import an OFX into a nYNAB budget  \r\n'
parser.add_argument('ofxfile', metavar='OFXPath', type=str,
                    help='The OFX file to import')
parser.add_argument('budgetname', metavar='BudgetName', type=str,
                    help='The nYNAB budget to use (creates it if it doesn''t exist')
parser.add_argument('accountname', metavar='AccountName', type=str, nargs='?',
                    help='The nYNAB account name  to use (creates it if it doesn''t exist')

args = parser.parse_known_args()[0]

connection = nYnabConnection(args.email, args.password)