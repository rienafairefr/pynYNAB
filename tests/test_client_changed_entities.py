import pytest
from mock import Mock

from pynYNAB.ClientFactory import BudgetClient
from pynYNAB.ObjClient import RootObjClient
from pynYNAB.schema import nYnabClient_
from pynYNAB.schema.budget import Account
from pynYNAB.schema.roots import Budget


@pytest.fixture
def obj(objclient, account):
    budget = objclient.obj
    budget.accounts = [account]
    account.parent = budget
    objclient.clear_changed_entities()
    return budget


@pytest.fixture
def objclient():
    client = Mock(spec=nYnabClient_)
    client.budget = Budget()
    obj_client = BudgetClient(client)
    return obj_client


@pytest.fixture
def account():
    return Account()


def test_get_ce_add(obj, objclient):
    added_account = Account()
    obj.accounts.append(added_account)
    changed_entities = objclient.get_changed_entities()
    assert changed_entities == {'accounts': {added_account.id:added_account}}


def test_get_ce_replace(obj, objclient, account):
    added_account = Account()
    obj.accounts = [added_account]
    changed_entities = objclient.get_changed_entities()
    removed_account = account.copy()
    removed_account.is_tombstone = True
    assert changed_entities == {'accounts': {added_account.id:added_account, removed_account.id:removed_account}}


def test_get_ce_delete(obj, objclient, account):
    obj.accounts.remove(account)
    changed_entities = objclient.get_changed_entities()
    deleted = account.copy()
    deleted.is_tombstone = True
    assert changed_entities == {'accounts': {deleted.id:deleted}}


def test_get_ce_modify(obj, objclient, account):
    account.account_name = 'BLA'
    changed_entities = objclient.get_changed_entities()
    assert changed_entities == {'accounts': {account.id:account}}


def test_get_ce_add_delete(obj, objclient):
    added_account = Account()
    obj.accounts.append(added_account)
    obj.accounts.remove(added_account)
    changed_entities = objclient.get_changed_entities()
    assert changed_entities == {}


def test_get_ce_delete_add(obj, objclient, account):
    obj.accounts.remove(account)
    obj.accounts.append(account)
    changed_entities = objclient.get_changed_entities()
    assert changed_entities == {}
