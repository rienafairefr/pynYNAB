import itertools
import random

from datetime import datetime

from pynYNAB.Client import clientfromargs
from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.config import parser

# used to ping the nYNAB API to check that the sync works

args = parser.parse_known_args()[0]
N=2
client = clientfromargs(args)
client.sync()
account = next(acc for acc in client.budget.be_accounts)
for _ in itertools.repeat(None, N):
    transaction = Transaction(
        cleared='Uncleared',
        date=datetime.now(),
        entities_account_id=account.id,
        amount=random.randrange(-10,10)
    )
    client.add_transaction(transaction)
    client.sync()
