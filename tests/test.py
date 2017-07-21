from __future__ import absolute_import

import datetime
import json
import unittest

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
from tests.common_mock import MockConnection


class MyEntity(Base, Entity):
    greatfield = Column(Integer, default=2)


class CommonTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')

        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

factory = nYnabClientFactory()


class TestGetChangedEntities(CommonTest):
    def setUp(self):
        super(TestGetChangedEntities, self).setUp()
        self.obj = Budget()
        self.account = Account()
        self.obj.be_accounts = [self.account]
        self.obj.clear_changed_entities()
        self.account2 = Account(id=self.account)

        self.client = factory.create_client(budget_name='budgetname', nynabconnection = MockConnection(),sync=False)

    def testgetChangedEntities_add(self):
        added_account = Account()
        self.obj.be_accounts.append(added_account)
        changed_entities = self.obj.get_changed_entities()
        self.assertEqual(changed_entities, {'be_accounts': [added_account]})

    def testgetChangedEntities_addtransactionsubtransaction(self):
        added_transaction = Transaction()
        subtransaction1 = Subtransaction(entities_transaction=added_transaction)
        subtransaction2 = Subtransaction(entities_transaction=added_transaction)

        self.client.budget.be_transactions.append(added_transaction)
        self.client.budget.be_subtransactions.append(subtransaction1)
        self.client.budget.be_subtransactions.append(subtransaction2)

        self.client.session.commit()

        changed_entities = self.client.budget.get_changed_entities()
        self.assertIsInstance(changed_entities,dict)
        self.assertEqual(1, len(changed_entities.keys()))
        self.assertEqual('be_transaction_groups',list(changed_entities.keys())[0])
        transaction_groups = changed_entities['be_transaction_groups']

        self.assertEqual(1, len(transaction_groups))
        self.assertEqual(added_transaction, transaction_groups[0]['be_transaction'])

        self.assertIsNotNone(transaction_groups[0]['be_subtransactions'])
        try:
            self.assertItemsEqual([subtransaction1,subtransaction2], set(transaction_groups[0]['be_subtransactions']))
        except AttributeError:
            self.assertCountEqual([subtransaction1,subtransaction2], set(transaction_groups[0]['be_subtransactions']))


    def testgetChangedEntities_delete(self):
        self.obj.be_accounts.remove(self.account)
        changed_entities = self.obj.get_changed_entities()
        deleted = self.account.copy()
        deleted.is_tombstone = True
        self.assertEqual(changed_entities, {'be_accounts': [deleted]})

    def testgetChangedEntities_modify(self):
        self.account.account_name = 'BLA'
        changed_entities = self.obj.get_changed_entities()
        self.assertEqual(changed_entities, {'be_accounts': [self.account]})

    def test_arraytype(self):
        user = User()
        user.feature_flags = ['featureA','feature1']
        self.session.add(user)
        self.session.commit()

        fetched_user = self.session.query(User).first()
        self.assertEqual(user,fetched_user)


class TestUpdateChangedEntities(CommonTest):
    def setUp(self):
        self.account = Account()

        self.client = factory.create_client(budgetname='budgetname', nynabconnection = MockConnection(),sync=False)
        self.client.budget.be_accounts = [self.account]
        self.account2 = self.account.copy()
        self.client.session.commit()

    def testupdateChangedEntities_add(self):
        new_account = Account()
        changed_entities = dict(
            be_accounts=[new_account]
        )
        self.client.budgetClient.update_from_changed_entities(changed_entities)
        self.assertEqual(len(self.client.budget.be_accounts), 2)
        self.assertIn(new_account, self.client.budget.be_accounts)

    def testupdateChangedEntities_delete(self):
        self.account2.is_tombstone = True
        changed_entities = dict(
            be_accounts=[self.account2]
        )
        self.client.budgetClient.update_from_changed_entities(changed_entities)
        self.assertEqual(len(self.client.budget.be_accounts), 0)

    def testupdateChangedEntities_modify(self):
        self.account2 = self.account.copy()
        self.account2.note = 'note'
        changed_entities = dict(
            be_accounts=[self.account2]
        )

        self.client.budgetClient.update_from_changed_entities(changed_entities)
        self.assertEqual(len(self.client.budget.be_accounts), 1)
        acc = self.client.budget.be_accounts[0]
        self.assertEqual(acc, self.account2)


class OtherTests(CommonTest):
    def testEntityjson(self):
        obj = MyEntity()
        self.session.add(obj)
        self.session.commit()

        jsonroundtrip = json.loads(json.dumps(obj, cls=ComplexEncoder))
        self.assertEqual({'id': str(obj.id), 'greatfield': 2, 'is_tombstone': False}, jsonroundtrip)

    def testequality(self):
        tr1 = Transaction(id='t')
        tr2 = Transaction(id='t')
        self.assertTrue(tr1 == tr2)

        tr1 = Transaction()
        tr2 = Transaction()
        self.assertFalse(tr1 == tr2)

    def testrepr(self):
        tr1 = Transaction(id='t')
        self.assertEqual(tr1.__repr__(),tr1.__str__())

    def testappend(self):
        obj = Budget()
        account = Account()
        obj.be_accounts.append(account)
        self.assertEqual(len(obj.be_accounts), 1)
        self.assertEqual(list(obj.be_accounts)[-1], account)

    def testappendBad(self):
        obj = Budget()
        transaction = Transaction()

        def testappend():
            obj.be_accounts.append(transaction)

        self.assertRaises(ValueError, testappend)

    def test_str(self):
        # tests no exceptions when getting the string representation of some entities
        obj = Transaction()
        obj.__str__()
        obj.__unicode__()

        obj2 = Budget()
        obj2.be_accounts.__str__()

    def jsondefault(self):
        encoded = json.dumps('test', cls=ComplexEncoder)
        self.assertEqual(encoded, 'test')


class TestOthers(unittest.TestCase):
    def test_copy(self):
        obj = Account()
        objc = obj.copy()
        self.assertEqual(obj.id, objc.id)
        self.assertEqual(obj.get_dict(), objc.get_dict())


class DummyEntity(Base, Entity):
    account_type = Column(Enum(AccountTypes), default=AccountTypes.undef)
    date = Column(Date)
    balance = Column(AmountType)


class TestApiDict(unittest.TestCase):
    def test_input(self):
        inputdict=dict(
            id='dummyid/ca85f126-04a1-4196-bbeb-a77acec4b28e',
            account_type='Checking',
            date='2016-10-01',
            balance=1000,
            is_tombstone=False
        )
        dummy = DummyEntity.from_apidict(inputdict)
        self.assertEqual(dummy.id,inputdict['id'])
        self.assertEqual(dummy.account_type,AccountTypes.Checking)
        self.assertEqual(dummy.date, datetime.date(year=2016,month=10,day=1))
        self.assertEqual(dummy.balance,1)

    def test_output(self):
        inputentity = DummyEntity(
            account_type = AccountTypes.Checking,
            date = datetime.date(year=2016,month=10,day=1),
            balance = 1
        )
        entitydict = inputentity.get_apidict()
        self.assertEqual(entitydict['id'], str(inputentity.id))
        self.assertEqual(entitydict['account_type'], 'Checking')
        self.assertEqual(entitydict['date'], '2016-10-01')
        self.assertEqual(entitydict['balance'], 1000)
