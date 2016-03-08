import json
import unittest

from pynYNAB.Entity import Entity, ComplexEncoder, ListofEntities, undef
from pynYNAB.budget import Account, AccountCalculation, AccountMapping, MasterCategory, Transaction, Subcategory, \
    MonthlyAccountCalculation, MonthlyBudget, MonthlySubcategoryBudget, MonthlyBudgetCalculation, \
    MonthlySubcategoryBudgetCalculation, PayeeLocation, Payee, PayeeRenameCondition, ScheduledSubtransaction, \
    ScheduledTransaction, Setting, Subtransaction, TransactionGroup
from pynYNAB.catalog import BudgetVersion, CatalogBudget, User, UserBudget, UserSetting
from pynYNAB.roots import Budget, Catalog
from pynYNAB.schema.Fields import EntityField, EntityListField


class Test1(unittest.TestCase):
    maxDiff = None

    def testEntityjson(self):
        class MyEntity(Entity):
            Fields = {'greatfield': EntityField(2)}

        obj = MyEntity()
        jsonroundtrip = json.loads(json.dumps(obj, cls=ComplexEncoder))
        assert (jsonroundtrip == {'id': obj.id, 'greatfield': 2})

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
            assert (isinstance(obj.AllFields, dict))
            for f in obj.AllFields:
                assert (isinstance(obj.AllFields[f], EntityField) or isinstance(obj.AllFields[f], EntityListField))
            assert (checkequal(obj.getdict().keys(), obj.AllFields.keys()))
            assert (checkequal(obj.getdict().values(), [getattr(obj, f) for f in obj.AllFields.keys()]))

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

    def testCE_nochange(self):
        obj = Transaction(None)
        self.assertEqual(obj.get_changed_entities(), {})

    def testCE_simpleadd(self):
        obj = Budget()
        account = Account()
        obj.be_accounts.append(account)
        self.assertEqual(obj.get_changed_entities(), {'be_accounts': [account]})

    def testCE_simpledelete(self):
        obj = Budget()
        account = Account()
        obj.be_accounts.delete(account)
        self.assertEqual(obj.get_changed_entities(), {'be_accounts': [account]})

    def testCE_simplechange(self):
        obj = Budget()
        account1 = Account()
        obj.be_accounts.append(account1)
        account2 = Account(id=account1.id, account_name='BLA')
        obj.be_accounts.changed = []
        obj.be_accounts.modify(account2)
        self.assertEqual(obj.get_changed_entities(), {'be_accounts': [account2]})

    def test_str(self):
        # tests no exceptions when getting the string representation of some entities
        obj = Transaction()
        obj.__str__()
        obj.__unicode__()

        obj2 = Budget()
        obj2.be_accounts.__str__()
        obj2.be_accounts.__unicode__()

    def testpropertyFields(self):
        obj = Entity()
        self.assertEqual(obj.Fields, {})

    def jsondefault(self):
        encoded = json.dumps('test', cls=ComplexEncoder)
        self.assertEqual(encoded, 'test')
