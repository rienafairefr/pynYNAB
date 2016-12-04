import json
import unittest

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pynYNAB.schema.Entity import Entity, ComplexEncoder, addprop, Base
from pynYNAB.schema.budget import Account, AccountCalculation, AccountMapping, MasterCategory, Transaction, SubCategory, \
    MonthlyAccountCalculation, MonthlyBudget, MonthlySubcategoryBudget, MonthlyBudgetCalculation, \
    MonthlySubcategoryBudgetCalculation, PayeeLocation, Payee, PayeeRenameCondition, ScheduledSubtransaction, \
    ScheduledTransaction, Setting, Subtransaction, TransactionGroup, Budget
from pynYNAB.schema.catalog import BudgetVersion, CatalogBudget, User, UserBudget, UserSetting, Catalog


class MyEntity(Base, Entity):
    greatfield = Column(Integer, default=2)


class CommonTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite://',echo=True)

        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()


class TestGetChangedEntities(CommonTest):
    def setUp(self):
        super(TestGetChangedEntities,self).setUp()
        self.obj = Budget()
        self.account = Account()
        self.obj.be_accounts = [self.account]
        self.account2 = Account(id=self.account.id)
        self.obj.clear_changed_entities()

    def testGetCE_add(self):
        added_account = Account()
        self.obj.be_accounts.append(added_account)
        changed_entities = self.obj.get_changed_entities()
        self.assertEqual(changed_entities, {'be_accounts': [added_account]})

    def testGetCE_delete(self):
        self.obj.be_accounts.remove(self.account)
        changed_entities = self.obj.get_changed_entities()
        deleted = self.account.copy()
        deleted.is_tombstone = True
        self.assertEqual(changed_entities, {'be_accounts': [deleted]})

    def testGetCE_change(self):
        self.account.account_name='BLA'
        changed_entities = self.obj.get_changed_entities()
        self.assertEqual(changed_entities, {'be_accounts': [self.account]})


class TestUpdateChangedEntities(CommonTest):
    def setUp(self):
        super(TestUpdateChangedEntities,self).setUp()
        self.obj = Budget()
        self.account = Account()
        self.obj.be_accounts = [self.account]
        self.account2 = self.account.copy()

    def testUpdateCE_add(self):
        new_account = Account()
        changed_entities = dict(
            be_accounts=[new_account]
        )
        self.obj.update_from_changed_entities(changed_entities)
        self.assertEqual(len(self.obj.be_accounts), 2)
        self.assertIn(new_account,self.obj.be_accounts)

    def testUpdateCE_delete(self):
        self.account2.is_tombstone = True
        changed_entities = dict(
            be_accounts=[self.account2]
        )
        self.obj.update_from_changed_entities(changed_entities)
        self.assertEqual(len(self.obj.be_accounts), 0)

    def testUpdateCE_modify(self):
        self.account2=self.account.copy()
        self.account2.direct_connect_account_id='s'
        changed_entities = dict(
            be_accounts=[self.account2]
        )
        self.obj.update_from_changed_entities(changed_entities)
        self.assertEqual(len(self.obj.be_accounts),1)
        acc = self.obj.be_accounts[0]
        self.assertEqual(acc.getdict(),self.account2.getdict())


class OtherTests(CommonTest):
    def testEntityjson(self):
        obj = MyEntity()
        self.session.add(obj)
        self.session.commit()

        jsonroundtrip = json.loads(json.dumps(obj, cls=ComplexEncoder))
        self.assertEqual({'id': str(obj.id), 'greatfield': 2, 'is_tombstone': False},jsonroundtrip)

    def testequality(self):
        tr1 = Transaction(id='t')
        tr2 = Transaction(id='t')
        self.assertEqual(tr1, tr2)

        tr1 = Transaction()
        tr2 = Transaction()
        self.assertNotEqual(tr1, tr2)

    def testappend(self):
        obj = Budget()
        account = Account()
        obj.be_accounts.append(account)
        self.assertEqual(len(obj.be_accounts) , 1)
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