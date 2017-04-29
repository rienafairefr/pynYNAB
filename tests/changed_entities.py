from pynYNAB.schema.Client import nYnabClient_
from pynYNAB.schema.budget import Account
from pynYNAB.schema.roots import Budget
from tests.test import CommonTest


class TestGetChangedEntities(CommonTest):
    def setUp(self):
        super(TestGetChangedEntities, self).setUp()
        self.obj = Budget()
        self.account = Account()
        self.obj.be_accounts = [self.account]
        self.obj.clear_changed_entities()
        self.account2 = Account(id=self.account)

    def testgetChangedEntities_add(self):
        added_account = Account()
        self.obj.be_accounts.append(added_account)
        changed_entities = self.obj.get_changed_entities()
        self.assertEqual(changed_entities, {'be_accounts': [added_account]})

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


class TestUpdateChangedEntities(CommonTest):
    def setUp(self):
        super(TestUpdateChangedEntities, self).setUp()
        self.account = Account()
        self.client = nYnabClient_(budgetname='Mock Budget')
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


