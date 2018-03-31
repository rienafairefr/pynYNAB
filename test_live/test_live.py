import random
import unittest

import pytest

from pynYNAB.ClientFactory import clientfromkwargs
from pynYNAB.schema import DictDiffer
from pynYNAB.schema.budget import Transaction
from pynYNAB.schema import *
from pynYNAB.schema.budget import Transaction, Account
from pynYNAB.scripts.helpers import merge_config
from tests.common import util_add_account


@pytest.fixture
def account(live_client_w_account):
    for account in live_client_w_account.budget.be_accounts:
        return account


@pytest.fixture
def live_client_w_account():
    live_client = reload()
    if len(live_client.budget.be_accounts) > 0:
        return live_client
    util_add_account(live_client, 'TestAccount')
    return live_client


def reload():
    config = merge_config()
    return clientfromkwargs(**config)


def test_add_deletetransaction(account, live_client_w_account):
    from datetime import datetime
    transaction = Transaction(
        amount=1,
        cleared='Uncleared',
        date=datetime.now(),
        entities_account_id=account.id,
    )
    client = live_client_w_account
    client.add_transaction(transaction)
    client = reload()
    assert transaction in client.budget.be_transactions
    client.delete_transaction(transaction)
    client = reload()
    assert transaction not in client.budget.be_transactions


def test_add_delete_account():
    from datetime import datetime
    account = Account(
        account_type=random.choice(list(AccountTypes)),
        account_name='test_account'
    )

    client = reload()
    client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())
    client = reload()
    assert account in client.budget.be_accounts
    client.delete_account(account)
    client = reload()
    assert account not in client.budget.be_transactions


@pytest.mark.parametrize(('obj_class', 'creator'), [
    (MasterCategory, lambda: MasterCategory(name='master_category'),),
    (AccountMapping, None),
    (Subtransaction, None),
    (ScheduledSubtransaction, None),
    (MonthlyBudget, None),
    (SubCategory, None),
    (PayeeLocation, None),
    (AccountCalculation, None),
    (MonthlyAccountCalculation, None),
    (MonthlySubcategoryBudgetCalculation, None),
    (ScheduledTransaction, None),
    (Payee, None),
    (MonthlySubcategoryBudget, None),
    (PayeeRenameCondition, None)
])
def test_add_delete_obj(obj_class, creator):
    client = reload()
    root = client.budget
    container = getattr(root, root.rev_listfields[obj_class])
    if creator is None:
        obj = obj_class()
    else:
        obj = creator()
    container.append(obj)
    client.push()

    client = reload()
    root = client.budget
    container = getattr(root, root.rev_listfields[obj_class])
    assert obj in container

    container.remove(obj)
    client.push()

    client = reload()
    root = client.budget
    container = getattr(root, root.rev_listfields[obj_class])
    assert obj not in container


if __name__ == "__main__":
    unittest.main()
