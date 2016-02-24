from Entity import Entity, EntityField, ComplexEncoder, EntityListField, ListofEntities, undef
import budget
import json
import unittest

class Test1(unittest.TestCase):
    maxDiff=None

    def successivesyncs(self):
        """
         >>> successivesyncs()
         0
         0
         0
        """
        #test succesive syncs

        import configparser
        import sys
        from budget import Transaction
        from nYNAB import nYNAB
        from nYNABConnection import nYNABConnection

        cp = configparser.ConfigParser()
        cp.read("ynab.conf")
        email = cp.get('AUTHENTICATION', 'email')
        password = cp.get('AUTHENTICATION', 'password')

        connection = nYNABConnection(email, password, reload=True)
        nYNABobject = nYNAB(connection, reload=True)

        print(nYNABobject.catalog.knowledge)
        nYNABobject.sync()
        print(nYNABobject.catalog.knowledge)
        nYNABobject.sync()
        print(nYNABobject.catalog.knowledge)

    def testEntityjson(self):

        class MyEntity(Entity):
            @property
            def Fields(self):
                return {'greatfield':EntityField(2)}
        obj=MyEntity()
        jsonroundtrip=json.loads(json.dumps(obj, cls=ComplexEncoder))
        assert(jsonroundtrip=={'id':obj.id,'greatfield': 2})

    def testListEntityjson(self):
        class MyEntity(Entity):
            @property
            def Fields(self):
                return {'accounts':EntityListField(budget.Account)}
        obj=MyEntity()
        account=budget.Account()
        obj.accounts.append(account)
        result=json.loads(json.dumps(obj, cls=ComplexEncoder))
        replacedundef={k:None if v==undef else v for k,v in account.getdict().iteritems() }
        expected={'accounts': [replacedundef],'id':obj.id}

        self.assertEqual(expected,result)

    def testimports(self):
        import budget
        import catalog
        types=[
            budget.Account,
            budget.AccountCalculation,
            budget.AccountMapping,
            budget.BudgetBudget,
            budget.MasterCategory,
            budget.MonthlyAccountCalculation,
            budget.MonthlyBudget,
            budget.MonthlyBudgetCalculation,
            budget.MonthlySubcategoryBudget,
            budget.MonthlySubcategoryBudgetCalculation,
            budget.Payee,
            budget.PayeeLocation,
            budget.PayeeRenameCondition,
            budget.ScheduledSubtransaction,
            budget.ScheduledTransaction,
            budget.Setting,
            budget.Subcategory,
            budget.Subtransaction,
            budget.Transaction,
            budget.TransactionGroup,
            catalog.BudgetVersion,
            catalog.Catalog,
            catalog.CatalogBudget,
            catalog.User,
            catalog.UserBudget,
            catalog.UserSetting
        ]
        def checkEqual(L1, L2):
            return len(L1) == len(L2) and sorted(L1) == sorted(L2)
        for typ in types:
            obj=typ()
            assert(isinstance(obj.AllFields,dict))
            for f in obj.AllFields:
                assert(isinstance(obj.AllFields[f],EntityField) or isinstance(obj.AllFields[f],EntityListField) )
            assert(checkEqual(obj.getdict().keys(),obj.AllFields.keys()))
            assert(checkEqual(obj.getdict().values(),[getattr(obj,f) for f in obj.AllFields.keys()]))

    def testupdatechangedentities(self):
        import budget
        obj=budget.BudgetBudget()
        assert(obj.be_accounts.__class__==ListofEntities)
        assert(obj.be_accounts.typeItems==budget.Account)
        assert(len(obj.be_accounts)==0)
        account=budget.Account()
        changed_entities=dict(
            be_accounts=[account]
        )
        obj.update_from_changed_entities(changed_entities)
        assert(len(obj.be_accounts) == 1)
        assert(obj.be_accounts[0].id==account.id)

    def testappend(self):

        obj=budget.BudgetBudget()
        account=budget.Account()
        obj.be_accounts.append(account)
        assert(len(obj.be_accounts)==1)
        assert(list(obj.be_accounts)[-1]==account)

    def testappendBad(self):
        import budget
        obj=budget.BudgetBudget()
        transaction=budget.Transaction()
        self.assertRaises(ValueError,lambda: obj.be_accounts.append(transaction))

    def testCE_nochange(self):
        obj1=budget.Transaction()
        obj2=budget.Transaction()
        self.assertEqual(obj2.get_changed_entities(obj1),{})

    def testCE_simpleadd(self):
        obj1=budget.BudgetBudget()
        obj2=budget.BudgetBudget()
        account=budget.Account()
        obj2.be_accounts.append(account)
        self.assertEqual(obj2.get_changed_entities(obj1) , {'be_accounts':[account]})

    def testCE_simpledelete(self):
        obj1=budget.BudgetBudget()
        obj2=budget.BudgetBudget()
        account=budget.Account()
        obj1.be_accounts.append(account)
        account.is_tombstone=True
        self.assertEqual(obj2.get_changed_entities(obj1) , {'be_accounts':[account]})

    def testCE_simplechange(self):
        obj1=budget.BudgetBudget()
        obj2=budget.BudgetBudget()
        account1=budget.Account()
        obj1.be_accounts.append(account1)
        account2=budget.Account(id=account1.id,account_name='BLA')
        obj2.be_accounts.append(account2)
        self.assertEqual(obj2.get_changed_entities(obj1) , {'be_accounts':[account2]})

    def testCE_bad(self):
        obj2=budget.BudgetBudget()
        self.assertIsNone(obj2.be_accounts.get_changed_entities(None))

    def test_str(self):
        obj=budget.Transaction()
        string1=obj.__str__()
        string2=obj.__unicode__()

        obj2=budget.BudgetBudget()
        string3=obj2.be_accounts.__str__()
        string4=obj2.be_accounts.__unicode__()
        pass
    def testpropertyFields(self):
        obj=Entity()
        self.assertEqual(obj.Fields,{})

    def jsondefault(self):
        encoded=json.dumps('test', cls=ComplexEncoder)
        self.assertEqual(encoded,'test')