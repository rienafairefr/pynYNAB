import pytest
from mock import Mock

from pynYNAB.ObjClient import RootObjClient
from pynYNAB.schema import nYnabClient_
from pynYNAB.schema.budget import Account
from pynYNAB.schema.roots import Budget


@pytest.fixture
def obj(account):
    budget = Budget()
    budget.be_accounts = [account]
    account.parent = budget
    return budget


@pytest.fixture
def objclient(obj):
    client = Mock(spec=nYnabClient_)
    obj_client = RootObjClient(obj, client, Budget)
    return obj_client


@pytest.fixture
def account():
    return Account()


def test_get_ce_add(obj, objclient):
    added_account = Account()
    obj.be_accounts.append(added_account)
    changed_entities = objclient.get_changed_entities()
    assert changed_entities == {'be_accounts': {added_account.id:added_account}}


def test_get_ce_replace(obj, objclient, account):
    added_account = Account()
    obj.be_accounts = [added_account]
    changed_entities = objclient.get_changed_entities()
    removed_account = account.copy()
    removed_account.is_tombstone = True
    assert changed_entities == {'be_accounts': {added_account.id:added_account, removed_account.id:removed_account}}


def test_get_ce_delete(obj, objclient, account):
    obj.be_accounts.remove(account)
    changed_entities = objclient.get_changed_entities()
    deleted = account.copy()
    deleted.is_tombstone = True
    assert changed_entities == {'be_accounts': {deleted.id:deleted}}


def test_get_ce_modify(obj, objclient, account):
    account.account_name = 'BLA'
    changed_entities = objclient.get_changed_entities()
    assert changed_entities == {'be_accounts': {account.id:account}}


def test_get_ce_add_delete(obj, objclient):
    added_account = Account()
    obj.be_accounts.append(added_account)
    obj.be_accounts.remove(added_account)
    changed_entities = objclient.get_changed_entities()
    assert changed_entities == {}


def test_get_ce_delete_add(obj, objclient, account):
    obj.be_accounts.remove(account)
    obj.be_accounts.append(account)
    changed_entities = objclient.get_changed_entities()
    assert changed_entities == {}
