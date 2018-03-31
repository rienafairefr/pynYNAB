import pytest

from pynYNAB.ClientFactory import clientfromkwargs
from pynYNAB.schema.budget import Account
from pynYNAB.schema.roots import Budget
from tests.common_mock import MockConnection
from tests.test_entities import session


@pytest.fixture
def client(account):
    client = clientfromkwargs(budget_name='Mock Budget', connection=MockConnection(), sync=False)
    client.budget.be_accounts = [account]
    return client


@pytest.fixture
def obj(account):
    budget = Budget()
    budget.be_accounts = [account]
    account.parent = budget
    budget.clear_changed_entities()
    return budget


@pytest.fixture
def account():
    return Account()


def test_get_ce_add(obj):
    added_account = Account()
    obj.be_accounts.append(added_account)
    changed_entities = obj.get_changed_entities()
    assert changed_entities == {'be_accounts': {added_account.id:added_account}}


def test_get_ce_replace(obj, account):
    added_account = Account()
    obj.be_accounts = [added_account]
    changed_entities = obj.get_changed_entities()
    removed_account = account.copy()
    removed_account.is_tombstone = True
    assert changed_entities == {'be_accounts': {added_account.id:added_account, removed_account.id:removed_account}}


def test_get_ce_delete(obj, account):
    obj.be_accounts.remove(account)
    changed_entities = obj.get_changed_entities()
    deleted = account.copy()
    deleted.is_tombstone = True
    assert changed_entities == {'be_accounts': {deleted.id:deleted}}


def test_get_ce_modify(obj, account):
    account.account_name = 'BLA'
    changed_entities = obj.get_changed_entities()
    assert changed_entities == {'be_accounts': {account.id:account}}


def test_get_ce_add_delete(obj):
    added_account = Account()
    obj.be_accounts.append(added_account)
    obj.be_accounts.remove(added_account)
    changed_entities = obj.get_changed_entities()
    assert changed_entities == {'be_accounts': {}}


def test_get_ce_delete_add(obj, account):
    obj.be_accounts.remove(account)
    obj.be_accounts.append(account)
    changed_entities = obj.get_changed_entities()
    assert changed_entities == {'be_accounts': {}}


def test_update_ce_add(client):
    new_account = Account()
    changed_entities = dict(
        be_accounts=[new_account]
    )
    client.budgetClient.update_from_changed_entities(changed_entities)
    assert len(client.budget.be_accounts) ==  2
    assert new_account in client.budget.be_accounts


def test_update_ce_delete(client, account):
    account2 = account.copy()
    account2.is_tombstone = True
    changed_entities = dict(
        be_accounts=[account2]
    )
    client.budgetClient.update_from_changed_entities(changed_entities)
    assert len(client.budget.be_accounts) == 0


def test_update_ce_modify(client, account):
    account2 = account.copy()
    account2.note = 'note'
    changed_entities = dict(
        be_accounts=[account2]
    )

    client.budgetClient.update_from_changed_entities(changed_entities)
    assert len(client.budget.be_accounts) == 1
    acc = client.budget.be_accounts[0]
    assert acc == account2