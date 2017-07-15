import random
from datetime import datetime

from pynYNAB.ClientFactory import clientfromargs
from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.__main__ import parser

# used to ping the nYNAB API to check that the sync works

args = parser.parse_known_args()[0]
N = 20
client = clientfromargs(args)
client.sync()
account = next(acc for acc in client.budget.be_accounts)
for _ in range(0, N):
    transaction = Transaction(
        cleared='Uncleared',
        date=datetime.now(),
        entities_account=account,
        amount=random.randrange(-10, 10)
    )
    client.add_transaction(transaction)
