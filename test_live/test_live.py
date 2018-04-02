import random

import pytest

from pynYNAB.ClientFactory import clientfromkwargs
from pynYNAB.schema import AccountTypes, KeyGenerator, datetime
from pynYNAB.schema.budget import Transaction, Account
from pynYNAB.scripts.helpers import merge_config
from tests.common import util_add_account
from datetime import datetime

@pytest.fixture
def account(live_client_w_account):
    for account in live_client_w_account.budget.be_accounts:
        return account


@pytest.fixture
def live_client():
    return reload()


@pytest.fixture
def live_client_w_account(live_client):
    if len(live_client.budget.be_accounts) > 0:
        return live_client
    util_add_account(live_client, 'TestAccount')
    return live_client


def reload():
    config = merge_config()
    return clientfromkwargs(**config)


def test_add_deletetransaction(account, live_client_w_account):
    transaction = Transaction(
        amount=1,
        cleared='Uncleared',
        date=datetime.now(),
        entities_account_id=account.id,
    )
    live_client_w_account.add_transaction(transaction)
    live_client_w_account = reload()
    assert transaction in live_client_w_account.budget.be_transactions
    live_client_w_account.delete_transaction(transaction)
    live_client_w_account = reload()
    assert transaction not in live_client_w_account.budget.be_transactions


def test_add_deleteaccount(live_client):
    account = Account(
        account_type=random.choice(list(AccountTypes)),
        account_name=KeyGenerator.generateuuid()
    )
    live_client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())
    live_client = reload()

    assert account in live_client.budget.be_accounts
    live_client.delete_account(account)
    live_client = reload()
    assert account not in live_client.budget.be_accounts
