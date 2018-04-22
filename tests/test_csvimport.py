import os
from datetime import datetime
from tempfile import gettempdir

import pytest

from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.__main__ import valid_schema
from pynYNAB.scripts.csvimport import do_csvimport, verify_csvimport, CsvImportArgs
from pynYNAB.utils import get_or_create_account, get_or_create_payee
from tests.common import util_add_account
from tests.common_mock import client


def ensure_has_account(client, account_name):
    for account in client.budget.accounts:
        if account_name is None or account.account_name == account_name:
            return client
    util_add_account(client, account_name)
    client.budgetClient.clear_changed_entities()
    return client


@pytest.fixture
def client_w_account_credit(client):
    return ensure_has_account(client, 'Credit')


@pytest.fixture
def client_w_account_cash(client):
    return ensure_has_account(client, 'Cash')


@pytest.fixture
def client_w_accounts(client):
    client = ensure_has_account(client, 'Cash')
    client = ensure_has_account(client, 'Credit')
    return ensure_has_account(client, 'Savings')


def get_transaction(client, date, payee, amount, memo, account):
    imported_date = datetime.now().date()
    return Transaction(
        entities_account_id=get_or_create_account(client, account).id,
        date=date,
        entities_payee_id=get_or_create_payee(client, payee).id,
        imported_payee=payee,
        source='Imported',
        memo=memo,
        amount=amount,
        cash_amount=amount,
        imported_date=imported_date
    )


def test_duplicate(client_w_account_credit):
    client = client_w_account_credit
    args = CsvImportArgs(os.path.join(gettempdir(), 'data.csv'), valid_schema('example'), None,
                         import_duplicates=False)

    content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Credit
"""
    with open(args.csv_file, mode='w') as f:
        f.writelines(content)

    transaction = get_transaction(client, datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20,
                                  'Buying pants',
                                  'Credit')
    client.budgetClient.clear_changed_entities()
    client.budget.transactions.append(transaction)
    verify_csvimport(args.schema, args.account_name)
    delta = do_csvimport(args, client)
    assert delta == 0


def test_duplicateForced(client_w_account_cash):
    client = client_w_account_cash
    args = CsvImportArgs(os.path.join(gettempdir(), 'data.csv'), valid_schema('example'), None, True)

    content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
"""
    with open(args.csv_file, mode='w') as f:
        f.writelines(content)

    transaction = get_transaction(client, datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20,
                                  'Buying pants',
                                  'Cash')

    client.budget.transactions.append(transaction)
    verify_csvimport(args.schema, args.account_name)
    delta = do_csvimport(args, client)
    assert delta == 1

    assert sum(1 for tr in client.budget.transactions if tr.key2 == transaction.key2) == 2


def test_import(client_w_accounts):
    client = client_w_accounts
    args = CsvImportArgs(os.path.join(gettempdir(), 'data.csv'), valid_schema('example'), import_duplicates=False)

    content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
2016-02-02,Thai Restaurant,-10,Food,Checking Account
2016-02-03,,10,Saving!,Savings
    """
    with open(args.csv_file, mode='w') as f:
        f.writelines(content)

    transactions = [
        get_transaction(client, datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants',
                        'Cash'),
        get_transaction(client, datetime(year=2016, month=2, day=2).date(), 'Thai Restaurant', -10, 'Food',
                        'Checking Account'),
        get_transaction(client, datetime(year=2016, month=2, day=3).date(), '', 10, 'Saving!', 'Savings'),
    ]

    verify_csvimport(args.schema, args.account_name)
    do_csvimport(args, client)
    for transaction in transactions:
        assert transaction.key2 in [tr.key2 for tr in client.budget.transactions]


__all__ = ['client']
