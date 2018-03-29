import pytest

from pynYNAB.ClientFactory import clientfromkwargs
from pynYNAB.schema import dict_merge
from pynYNAB.schema.budget import Account
from pynYNAB.schema.roots import Budget
from tests.common_mock import MockConnection
from tests.test_entities import session
from tests.test_changed_entities import client, obj, account




def test_get_ce_add(obj):
    added_account = Account()
    obj.be_accounts.append(added_account)
    changed_entities = obj.get_changed_entities_dict()
    assert changed_entities == {'be_accounts': [added_account.get_dict()]}


def test_get_ce_replace(obj, account):
    added_account = Account()
    obj.be_accounts = [added_account]
    changed_entities = obj.get_changed_entities_dict()
    removed_account = dict_merge(account.get_dict(), {'is_tombstone':True})
    assert changed_entities == {'be_accounts': [added_account.get_dict(), removed_account]}


def test_get_ce_delete(obj, account):
    obj.be_accounts.remove(account)
    changed_entities = obj.get_changed_entities_dict()
    deleted = dict_merge(account.get_dict(), {'is_tombstone':True})
    assert changed_entities == {'be_accounts': [deleted]}


def test_get_ce_modify(obj, account):
    account.account_name = 'BLA'
    changed_entities = obj.get_changed_entities_dict()
    assert changed_entities == {'be_accounts': [account.get_dict()]}