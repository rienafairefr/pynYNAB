import random
from datetime import datetime, timedelta

from pynYNAB import KeyGenerator
from pynYNAB.schema.Entity import AccountTypes
from pynYNAB.schema.budget import Transaction, Account, Subtransaction, Payee
from test_live.common import CommonLive
from test_live.common import needs_account


# noinspection PyArgumentList
class LiveTests(CommonLive):
    def test_add_delete_budget(self):
        budget_name = str(KeyGenerator.generateuuid())
        self.client.create_budget(budget_name)
        self.reload()
        matches = [b for b in self.client.catalog.ce_budgets if b.budget_name == budget_name]
        self.assertTrue(len(matches) == 1)
        self.client.delete_budget(budget_name)
        self.reload()
        matches = [b for b in self.client.catalog.ce_budgets if b.budget_name == budget_name]
        self.assertTrue(len(matches) == 0)
        self.reload()

    def test_add_delete_account(self):
        account_type = AccountTypes.Checking
        account_name = str(KeyGenerator.generateuuid())
        budget = self.client.budget

        for account in budget.be_accounts:
            if account.account_name == account_name:
                return
        if len(budget.be_accounts) > 0:
            sortable_index = max(account.sortable_index for account in budget.be_accounts)
        else:
            sortable_index = 0

        account = Account(
            account_type=account_type,
            account_name=account_name,
            sortable_index=sortable_index,
            on_budget=True
        )

        self.client.add_account(account, balance=123.45, balance_date=datetime.now())
        self.reload()
        self.assertIn(account, self.client.budget.be_accounts)
        self.client.delete_account(account)
        self.reload()
        self.assertNotIn(account, self.client.budget.be_accounts)

    @needs_account()
    def test_add_deletetransaction(self):
        from datetime import datetime
        transaction = Transaction(
            amount=1,
            cleared='Uncleared',
            date=datetime.now(),
            entities_account_id=self.account.id,
        )
        self.client.add_transaction(transaction)
        self.reload()
        self.assertIn(transaction, self.client.budget.be_transactions)
        self.client.delete_transaction(transaction)
        self.reload()
        self.assertNotIn(transaction, self.client.budget.be_transactions)

    @needs_account('account1')
    @needs_account('account2')
    def test_add_transfer(self):
        account1 = next(account for account in self.client.budget.be_accounts if account.account_name == 'account1')
        account2 = next(account for account in self.client.budget.be_accounts if account.account_name == 'account2')

        try:
            payee_2 = next(payee for payee in self.client.budget.be_payees if payee.entities_account_id == account2.id)
        except StopIteration:
            payee_2 = Payee(entities_account=account2)
            self.client.budget.be_payees.append(payee_2)
        try:
            payee_1 = next(payee for payee in self.client.budget.be_payees if payee.entities_account_id == account1.id)
        except StopIteration:
            payee_1 = Payee(entities_account=account1)
            self.client.budget.be_payees.append(payee_1)

        transaction1 = Transaction(
            amount=random.randint(-10, 10),
            date=datetime.now(),
            entities_account=account1,
            entities_payee=payee_2
        )
        transaction2 = Transaction(
            amount=-transaction1.amount,
            date=datetime.now(),
            entities_account=account2,
            entities_payee=payee_1
        )
        self.client.budget.be_transactions.append(transaction1)
        self.client.budget.be_transactions.append(transaction2)
        self.client.sync()
        self.reload()
        self.assertIn(transaction1, self.client.budget.be_transactions)
        self.assertIn(transaction2, self.client.budget.be_transactions)
        self.client.budget.be_transactions.remove(transaction1)
        self.client.budget.be_transactions.remove(transaction2)
        self.client.sync()

    @needs_account()
    def test_add_deletetransactions(self):
        from datetime import datetime

        transactions = [
            Transaction(
                amount=random.randint(-10, 10),
                cleared='Uncleared',
                date=datetime.now() - 8 * timedelta(days=365),
                entities_account_id=self.account.id,
            ), Transaction(
                amount=random.randint(-10, 10),
                cleared='Uncleared',
                date=datetime.now() + 8 * timedelta(days=365),
                entities_account_id=self.account.id,
            ), Transaction(
                amount=random.randint(-10, 10),
                cleared='Uncleared',
                date=datetime.now(),
                entities_account_id=self.account.id,
            )
        ]

        self.client.add_transactions(transactions)
        print('Time for request: ' + str(self.client.connection.lastrequest_elapsed.total_seconds()) + ' s')
        self.reload()
        for transaction in transactions:
            self.assertIn(transaction, self.client.budget.be_transactions)
        for transaction in transactions:
            self.client.delete_transaction(transaction)
        self.reload()
        for transaction in transactions:
            self.assertNotIn(transaction, self.client.budget.be_transactions)

    @needs_account()
    def test_add_splittransactions(self):
        subcatsplit = next(subcategory for subcategory in self.client.budget.be_subcategories if
                           subcategory.internal_name == 'Category/__Split__')
        transaction = Transaction(
            amount=1,
            date=datetime.now(),
            entities_account=self.account,
            entities_subcategory=subcatsplit
        )
        cat1 = self.client.budget.be_subcategories[0]
        cat2 = self.client.budget.be_subcategories[1]

        sub1 = Subtransaction(
            amount=0.5,
            entities_transaction=transaction,
            entities_subcategory=cat1
        )
        sub2 = Subtransaction(
            amount=0.5,
            entities_transaction=transaction,
            entities_subcategory=cat2
        )
        self.client.budget.be_transactions.append(transaction)
        self.client.budget.be_subtransactions.append(sub1)
        self.client.budget.be_subtransactions.append(sub2)
        self.client.sync()
        self.reload()
        self.assertIn(transaction, self.client.budget.be_transactions)
        self.assertIn(sub1, self.client.budget.be_subtransactions)
        self.assertIn(sub2, self.client.budget.be_subtransactions)
