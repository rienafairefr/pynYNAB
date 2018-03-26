from __future__ import absolute_import

import datetime
import json
from collections import namedtuple

import pytest
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.schema.Entity import Entity, ComplexEncoder, Base, AccountTypes
from pynYNAB.schema.budget import Account, Transaction, Subtransaction
from pynYNAB.schema.catalog import User
from pynYNAB.schema.roots import Budget
from pynYNAB.schema.types import AmountType
from .common_mock import MockConnection


class MyEntity(Base, Entity):
    greatfield = Column(Integer, default=2)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


@pytest.fixture
def account():
    return Account()


@pytest.fixture
def client(account):
    client = nYnabClientFactory().create_client(budget_name='budgetname',
                                                connection=MockConnection(),
                                                sync=False)
    client.budget.be_accounts = [account]
    client.session.commit()
    client.budget.clear_changed_entities()
    return client


@pytest.fixture
def obj_w_account(account):
    ObjWAccount = namedtuple('ObjWAccount', ['obj', 'account'])
    budget = Budget()
    budget.be_accounts = [account]
    budget.clear_changed_entities()
    return ObjWAccount(budget, account)


@pytest.fixture
def obj(account):
    budget = Budget()
    budget.be_accounts = [account]
    budget.clear_changed_entities()
    return budget


def test_get_ce_addtransactionsubtransaction(client):
    added_transaction = Transaction()
    subtransaction1 = Subtransaction(entities_transaction=added_transaction)
    subtransaction2 = Subtransaction(entities_transaction=added_transaction)

    client.budget.be_transactions.append(added_transaction)
    client.budget.be_subtransactions.append(subtransaction1)
    client.budget.be_subtransactions.append(subtransaction2)

    client.session.commit()

    changed_entities = client.budget.get_changed_entities()
    assert isinstance(changed_entities, dict)
    assert 1 == len(changed_entities.keys())
    assert 'be_transaction_groups' == list(changed_entities.keys())[0]
    transaction_groups = changed_entities['be_transaction_groups']

    assert 1 == len(transaction_groups)
    assert added_transaction == transaction_groups[0]['be_transaction']

    assert transaction_groups[0]['be_subtransactions'] is not None
    try:
        assert {subtransaction1, subtransaction2} == set(transaction_groups[0]['be_subtransactions'])
    except AttributeError:
        assert len([subtransaction1, subtransaction2]) == len(set(transaction_groups[0]['be_subtransactions']))


def test_arraytype(session):
    user = User()
    user.feature_flags = ['featureA', 'feature1']
    session.add(user)
    session.commit()

    fetched_user = session.query(User).first()
    assert user == fetched_user


def test_Entityjson(session):
    obj = MyEntity()
    session.add(obj)
    session.commit()

    jsonroundtrip = json.loads(json.dumps(obj, cls=ComplexEncoder))
    assert {'id': str(obj.id), 'greatfield': 2, 'is_tombstone': False} == jsonroundtrip


def test_equality():
    tr1 = Transaction(id='t')
    tr2 = Transaction(id='t')
    assert tr1 == tr2

    tr1 = Transaction()
    tr2 = Transaction()
    assert tr1 != tr2


def test_repr():
    tr1 = Transaction(id='t')
    assert tr1.__repr__() == tr1.__str__()


def test_append():
    obj = Budget()
    account = Account()
    obj.be_accounts.append(account)
    assert len(obj.be_accounts) == 1
    assert list(obj.be_accounts)[-1] == account


def test_str():
    # tests no exceptions when getting the string representation of some entities
    obj = Transaction()
    obj.__str__()
    obj.__unicode__()

    obj2 = Budget()
    obj2.be_accounts.__str__()


def test_copy():
    obj = Account()
    objc = obj.copy()
    assert obj.id == objc.id
    assert obj.get_dict() == objc.get_dict()


class DummyEntity(Base, Entity):
    account_type = Column(Enum(AccountTypes), default=AccountTypes.undef)
    date = Column(Date)
    balance = Column(AmountType)


def test_input():
    inputdict = dict(
        id='dummyid/ca85f126-04a1-4196-bbeb-a77acec4b28e',
        account_type='Checking',
        date='2016-10-01',
        balance=1000,
        is_tombstone=False
    )
    dummy = DummyEntity.from_apidict(inputdict)
    assert dummy.id == inputdict['id']
    assert dummy.account_type == AccountTypes.Checking
    assert dummy.date, datetime.date(year=2016, month=10, day=1)
    assert dummy.balance == 1


def test_output():
    inputentity = DummyEntity(
        account_type=AccountTypes.Checking,
        date=datetime.date(year=2016, month=10, day=1),
        balance=1
    )
    entitydict = inputentity.get_apidict()
    assert entitydict['id'] == str(inputentity.id)
    assert entitydict['account_type'] == 'Checking'
    assert entitydict['date'] == '2016-10-01'
    assert entitydict['balance'] == 1000
