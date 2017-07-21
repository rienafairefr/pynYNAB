from dotenv import load_dotenv,find_dotenv

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.connection import nYnabConnection
from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.__main__ import parser

load_dotenv(find_dotenv())

print('test_sync')
args = parser.parse_known_args()[0]

connection = nYnabConnection(args.email,args.password)
args.connection = connection

client = nYnabClientFactory().create_client(args)
client.sync()

for i in range(0,1000):
    client.budget.be_transactions.append(Transaction())
client.push(1000)
print('OK')
