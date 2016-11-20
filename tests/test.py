import json
import unittest

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pynYNAB.schema.Entity import Entity, ComplexEncoder, ListofEntities, addprop, Base
from pynYNAB.schema.Fields import EntityField, EntityListField, PropertyField
from pynYNAB.schema.budget import Account, AccountCalculation, AccountMapping, MasterCategory, Transaction, Subcategory, \
    MonthlyAccountCalculation, MonthlyBudget, MonthlySubcategoryBudget, MonthlyBudgetCalculation, \
    MonthlySubcategoryBudgetCalculation, PayeeLocation, Payee, PayeeRenameCondition, ScheduledSubtransaction, \
    ScheduledTransaction, Setting, Subtransaction, TransactionGroup, Budget
from pynYNAB.schema.catalog import BudgetVersion, CatalogBudget, User, UserBudget, UserSetting, Catalog


class MyEntity(Base, Entity):
    greatfield = Column(Integer, default=2)

class Test1(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        engine = create_engine('sqlite://',echo=True)

        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def testEntityjson(self):
        obj = MyEntity()
        self.session.add(obj)
        self.session.commit()

        jsonroundtrip = json.loads(json.dumps(obj, cls=ComplexEncoder))
        self.assertEqual({'id': str(obj.id), 'greatfield': 2},jsonroundtrip)

    def testequality(self):
        tr1 = Transaction()
        tr2 = Transaction()
        self.assertNotEqual(tr1, tr2)

        tr1 = Transaction(entities_account_id=1)
        tr2 = Transaction(entities_account_id=2)
        self.assertNotEqual(tr1, tr2)

    def testentityIn(self):
        tr1 = Transaction()
        transactions = ListofEntities(Transaction)
        transactions.append(tr1)
        self.assertIn(tr1, transactions)

    def testentityIn2(self):
        tr1 = Transaction()
        tr2 = Transaction()
        transactions = ListofEntities(Transaction)
        transactions.append(tr1)
        self.assertNotIn(tr2, transactions)

    def test_hash(self):
        tr1 = Transaction()
        result = tr1._hash()
        self.assertIsInstance(result, int)

    def testprop(self):

        namefield = 'p'
        default = lambda self: self.y

        def pgetter(self):
            if hasattr(self, '__prop_' + namefield):
                return getattr(self, '__prop_' + namefield)
            else:
                return default(self)

        def psetter(self, value):
            setattr(self, '__prop_' + namefield, value)

        class myClass(object):
            y = 1

        obj1 = myClass()
        addprop(obj1, namefield, pgetter, psetter)

        self.assertEqual(obj1.p, 1)
        obj1.y = 3
        self.assertEqual(obj1.p, 3)
        obj1.p = 5
        self.assertEqual(obj1.p, 5)
        obj1.y = 7
        self.assertNotEqual(obj1.p, 7)

    def test_lambdaprop(self):
        class MockEntity(Entity):
            input = EntityField(True),
            override = PropertyField(lambda x: x.input)

        # override behaves like a @property attribute:

        entity1 = MockEntity()
        self.assertEqual(entity1.override, entity1.input)
        entity1.input = False
        self.assertEqual(entity1.override, entity1.input)
        entity1.input = 12
        self.assertEqual(entity1.override, entity1.input)

        # unless set directly:

        entity1.override = 42
        self.assertEqual(entity1.override, 42)
        # then it behaves like a normal attribute:
        entity1.input = False
        self.assertEqual(entity1.override, 42)

        # we can clear and come back to @property behavior
        entity1.clean_override()

        self.assertEqual(entity1.override, entity1.input)
        entity1.input = False
        self.assertEqual(entity1.override, entity1.input)
        entity1.input = 12
        self.assertEqual(entity1.override, entity1.input)

    def testimports(self):
        types = [
            Account,
            AccountCalculation,
            AccountMapping,
            Budget,
            MasterCategory,
            MonthlyAccountCalculation,
            MonthlyBudget,
            MonthlyBudgetCalculation,
            MonthlySubcategoryBudget,
            MonthlySubcategoryBudgetCalculation,
            Payee,
            PayeeLocation,
            PayeeRenameCondition,
            ScheduledSubtransaction,
            ScheduledTransaction,
            Setting,
            Subcategory,
            Subtransaction,
            Transaction,
            TransactionGroup,
            BudgetVersion,
            Catalog,
            CatalogBudget,
            User,
            UserBudget,
            UserSetting
        ]

        def checkequal(l1, l2):
            return len(l1) == len(l2) and sorted(l1) == sorted(l2)

        for typ in types:
            obj = typ()
            self.assertIsInstance(obj.AllFields, dict)
            for f in obj.AllFields:
                self.assertTrue(
                    isinstance(obj.AllFields[f], EntityField) or isinstance(obj.AllFields[f], EntityListField))
            self.assertTrue(checkequal(obj.getdict().keys(), obj.AllFields.keys()))

            valuesleft = list(obj.getdict().values())
            valuesright = [getattr(obj, f) for f in obj.AllFields.keys()]

            unhashableleft = [v for v in valuesleft if v.__hash__ is None]
            hashableleft = [v for v in valuesleft if v.__hash__ is not None]

            unhashableright = [v for v in valuesright if v.__hash__ is None]
            hashableright = [v for v in valuesright if v.__hash__ is not None]
            self.assertEqual(set(hashableleft), set(hashableright))
            self.assertEqual(unhashableleft, unhashableright)

    def testupdatechangedentities(self):
        obj = Budget()
        assert (obj.be_accounts.__class__ == ListofEntities)
        assert (obj.be_accounts.typeItems == Account)
        assert (len(obj.be_accounts) == 0)
        account = Account()
        changed_entities = dict(
            be_accounts=[account]
        )
        obj.update_from_changed_entities(changed_entities)
        assert (len(obj.be_accounts) == 1)
        assert (next(obj.be_accounts.__iter__()) == account)

    def testappend(self):

        obj = Budget()
        account = Account(None)
        obj.be_accounts.append(account)
        assert (len(obj.be_accounts) == 1)
        assert (list(obj.be_accounts)[-1] == account)

    def testappendBad(self):
        obj = Budget()
        transaction = Transaction()
        self.assertRaises(ValueError, lambda: obj.be_accounts.append(transaction))

    def testCE_simpleadd(self):
        obj = Budget()
        account = Account()
        obj.be_accounts.append(account)
        self.assertEqual(obj.get_changed_entities(), {'be_accounts': [account]})

    def testCE_simpledelete(self):
        obj = Budget()
        account = Account()
        obj.be_accounts.append(account)
        obj.__changed = None
        obj.be_accounts.remove(account)
        self.assertEqual(obj.get_changed_entities(), {'be_accounts': [account]})

    def testCE_simplechange(self):
        obj = Budget()
        account1 = Account()
        obj.be_accounts.append(account1)
        self.session.add(obj)
        self.session.commit()

        account1.account_name='BLA'
        changed_entities = obj.get_changed_entities()
        self.assertEqual(changed_entities, {'be_accounts': [account1]})

    def test_str(self):
        # tests no exceptions when getting the string representation of some entities
        obj = Transaction()
        obj.__str__()
        obj.__unicode__()

        obj2 = Budget()
        obj2.be_accounts.__str__()
        obj2.be_accounts.__unicode__()

    def jsondefault(self):
        encoded = json.dumps('test', cls=ComplexEncoder)
        self.assertEqual(encoded, 'test')
