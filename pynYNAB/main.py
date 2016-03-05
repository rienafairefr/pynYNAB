# coding=utf-8
import random

from Client import nYnabClient
from budget import Transaction
from config import email, password
from connection import nYnabConnection


if __name__ == "__main__":
    connection = nYnabConnection(email, password, reload=True)
    nYNABobject = nYnabClient(connection, budget_name='My Budget', reload=True)

    from datetime import datetime

    for account in nYNABobject.budget.be_accounts:
        if not account.is_tombstone:
            n = 3
            transactions=[]
            for i in range(n):
                transactions.append(Transaction(
                    amount=random.randint(-10,10),
                    cleared='Uncleared',
                    date=datetime.now(),
                    entities_account_id=account.id,
                ))
            nYNABobject.add_transactions(transactions)
            exit(0)
    raise ValueError('No available account !')

