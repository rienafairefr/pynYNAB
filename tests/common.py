import random
from datetime import datetime
from functools import wraps

from pynYNAB import KeyGenerator
from pynYNAB.schema import Account, AccountTypes


def util_add_account(client, account_name=None):
    if account_name is None:
        account_name = str(KeyGenerator.generateuuid())
    account = Account(
        account_type=random.choice(list(AccountTypes)),
        account_name=account_name
    )

    client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())
    return account
