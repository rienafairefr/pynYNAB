from datetime import datetime

from dotenv import load_dotenv,find_dotenv

from pynYNAB.ClientFactory import clientfromargs
from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.__main__ import parser
from pynYNAB.utils import get_or_create_payee

load_dotenv(find_dotenv())

print('test_sync')
args = parser.parse_known_args()[0]
client = clientfromargs(args)
client.sync()

accounts = {v.account_name:v for v in client.budget.be_accounts}
payees = {p.name:p for p in client.budget.be_payees}
listaccounts = list(accounts.values())
account0 = listaccounts[0]
account1 = listaccounts[1]

transactions = []

account_id = account0.id
transfer_id = account1.id

# Payees:  "Transfer : account_name"
account_payee_id = payees['Transfer : ' + account1.account_name].id
transfer_payee_id = payees['Transfer : ' + account0.account_name].id

imported_date = datetime.now().date()

payee_name = 'Payee'
payee = get_or_create_payee(client, payee_name)
payee_id = payee.id

amount = 10
date = datetime(2016,10,5).date()


transaction_1 = Transaction(
    entities_account_id=account_id,
    entities_payee_id=account_payee_id,
    amount=amount,
    date=date,
    imported_date=imported_date,
    imported_payee=payee_name,
    source='Matched',
    cash_amount=amount
)

transaction_orig = Transaction(
    entities_account_id=account_id,
    amount=amount,
    date=date,
    entities_payee_id=payee_id,
    imported_date=imported_date,
    memo="",
    source='matched_import'
)

# match
transaction_1.matched_transaction_id = transaction_orig.id
transaction_orig.matched_transaction_id = transaction_1.id

transactions.append(transaction_orig)
transactions.append(transaction_1)

client.add_transactions(transactions)