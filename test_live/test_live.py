import unittest

import pytest

from pynYNAB.ClientFactory import clientfromkwargs
from pynYNAB.schema import DictDiffer
from pynYNAB.schema.budget import Transaction
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


if __name__ == "__main__":
    unittest.main()
