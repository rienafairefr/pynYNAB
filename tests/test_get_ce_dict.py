from pynYNAB.schema import dict_merge
from pynYNAB.schema.budget import Account
from tests.test_entities import session
from tests.test_changed_entities import client, obj, account


def _m(it):
    return {el.id:el.get_dict() for el in it}


def test_get_ce_add(obj):
    added_account = Account()
    obj.be_accounts.append(added_account)
    changed_entities = obj.get_changed_entities_dict()
    assert changed_entities == {'be_accounts': _m([added_account])}


def test_get_ce_replace(obj, account):
    added_account = Account()
    obj.be_accounts = [added_account]
    changed_entities = obj.get_changed_entities_dict()
    removed_account = account.copy()
    removed_account.is_tombstone = True
    assert changed_entities == {'be_accounts': _m([added_account, removed_account])}


def test_get_ce_delete(obj, account):
    obj.be_accounts.remove(account)
    changed_entities = obj.get_changed_entities_dict()
    deleted = account.copy()
    deleted.is_tombstone= True
    assert changed_entities == {'be_accounts': _m([deleted])}


def test_get_ce_modify(obj, account):
    account.account_name = 'BLA'
    changed_entities = obj.get_changed_entities_dict()
    assert changed_entities == {'be_accounts': _m([account])}


def test_get_ce_add_delete(obj):
    added_account = Account()
    obj.be_accounts.append(added_account)
    obj.be_accounts.remove(added_account)
    changed_entities = obj.get_changed_entities_dict()
    assert changed_entities == {'be_accounts': {}}


def test_get_ce_delete_add(obj, account):
    obj.be_accounts.remove(account)
    obj.be_accounts.append(account)
    changed_entities = obj.get_changed_entities_dict()
    assert changed_entities == {'be_accounts': {}}

