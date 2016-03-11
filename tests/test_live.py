import random
from datetime import datetime, timedelta
from functools import wraps

from pynYNAB import KeyGenerator
from pynYNAB.Entity import AccountTypes
from pynYNAB.budget import Transaction, Account, Subtransaction

from tests.common_Live import commonLive


class liveTests(commonLive):
    def test_add_delete_budget(self):
        budget_name=KeyGenerator.generateuuid()
        self.client.create_budget(budget_name)
        self.reload()
        matches=[b for b in self.client.catalog.ce_budgets if b.budget_name==budget_name]
        self.assertTrue(len(matches) == 1)
        self.client.delete_budget(budget_name)
        self.reload()
        matches=[b for b in self.client.catalog.ce_budgets if b.budget_name==budget_name]
        self.assertTrue(len(matches) == 0)
        self.reload()

    def needs_account(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            for account in self.client.budget.be_accounts:
                self.account = account
                fn(self, *args, **kwargs)
                return
            self.util_add_account()
            raise ValueError('No available account !')
        return wrapped

    def needs_transaction(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            for transaction in self.client.budget.be_transactions:
                if transaction.entities_account_id == self.account.id:
                    self.transaction = transaction
                    fn(self, *args, **kwargs)
                    return
            self.util_add_transaction()
            raise ValueError('No available transaction !')

        return wrapped

    def test_add_delete_account(self):
        account_type=AccountTypes.Checking
        account_name = KeyGenerator.generateuuid()
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
        )

        self.client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())

        self.reload()

        self.assertIn(account, self.client.budget.be_accounts)

        self.client.delete_account(account)

        self.reload()

        result = self.client.budget.be_transactions.get(account.id)

        self.assertTrue(result is None)

    def test_add_transaction_amount_alltypes(self):
        amount0=10
        for account_type in AccountTypes:
            account=Account(
                account_type=account_type,
                account_name=KeyGenerator.generateuuid()
            )
            self.client.add_account(account, balance=0, balance_date=datetime.now())
            tr=Transaction(
                entities_account_id=account.id,
                amount=amount0,
                cleared='Uncleared',
                date=datetime.now(),
            )
            self.client.add_transaction(tr)
            self.reload()
            self.client.delete_account(account)
            print(account.account_type)
            print((self.client.budget.be_transactions.get(tr.id).amount,self.client.budget.be_transactions.get(tr.id).cash_amount,self.client.budget.be_transactions.get(tr.id).credit_amount))
            self.assertEqual(self.client.budget.be_transactions.get(tr.id).amount,amount0)
            self.assertEqual(self.client.budget.be_transactions.get(tr.id).cash_amount,amount0)
            self.assertEqual(self.client.budget.be_transactions.get(tr.id).credit_amount,0)

    def test_add_delete_account_alltypes(self):
        for account_type in AccountTypes:
            account_name = KeyGenerator.generateuuid()
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
            )

            self.client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())

            self.reload()

            self.assertIn(account, self.client.budget.be_accounts)

            self.client.delete_account(account)

            self.reload()

            result = self.client.budget.be_transactions.get(account.id)

            self.assertTrue(result is None)

    @needs_account
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

        result = self.client.budget.be_transactions.get(transaction.id)
        self.assertTrue(result is None)

    @needs_account
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
            )]

        n = 3
        for i in range(len(transactions) - n):
            transactions.append(Transaction(
                amount=random.randint(-10, 10),
                cleared='Uncleared',
                date=datetime.now(),
                entities_account_id=self.account.id,
            ))
        self.client.add_transactions(transactions)
        print('Time for request: ' + str(self.client.connection.lastrequest_elapsed.total_seconds()) + ' s')

        self.reload()
        for transaction in transactions:
            self.assertIn(transaction, self.client.budget.be_transactions)

        for transaction in transactions:
            self.client.delete_transaction(transaction)
        self.reload()

        for transaction in transactions:
            resulttransaction = self.client.budget.be_transactions.get(transaction.id)
            self.assertTrue(resulttransaction is None)


    @needs_account
    def test_add_splittransactions(self):
        subcatsplit_id = next(subcategory.id for subcategory in self.client.budget.be_subcategories if
                              subcategory.internal_name == 'Category/__Split__')
        transaction = Transaction(
            amount=1,
            date=datetime.now(),
            entities_account_id=self.account.id,
            entities_subcategory_id=subcatsplit_id
        )
        sub1 = Subtransaction(
            amount=5000,
            entities_transaction_id=transaction.id
        )
        sub2 = Subtransaction(
            amount=5000,
            entities_transaction_id=transaction.id
        )
        self.client.budget.be_transactions.append(transaction)
        self.client.budget.be_subtransactions.append(sub1)
        self.client.budget.be_subtransactions.append(sub2)

        self.client.sync()

        self.reload()

        self.assertIn(transaction, self.client.budget.be_transactions)
        self.assertIn(sub1, self.client.budget.be_subtransactions)
        self.assertIn(sub2, self.client.budget.be_subtransactions)

    @needs_account
    @needs_transaction
    def test_split(self):
        subcat1, subcat2 = tuple(random.sample(list(self.client.budget.be_subcategories), 2))
        subcatsplit_id = next(subcategory.id for subcategory in self.client.budget.be_subcategories if
                              subcategory.internal_name == 'Category/__Split__')
        self.transaction.entities_subcategory_id = subcatsplit_id

        sub1 = Subtransaction(
            amount=self.transaction.amount - 5000,
            entities_transaction_id=self.transaction.id,
            entities_subcategory_id=subcat1.id
        )
        sub2 = Subtransaction(
            amount=5000,
            entities_transaction_id=self.transaction.id,
            entities_subcategory_id=subcat2.id
        )

        self.client.budget.be_subtransactions.append(sub1)
        self.client.budget.be_subtransactions.append(sub2)
        self.client.budget.be_transactions.modify(self.transaction)

        self.client.sync()

        self.reload()

        self.assertIn(sub1, self.client.budget.be_subtransactions)
        self.assertIn(self.transaction, self.client.budget.be_transactions)
        self.assertIn(sub2, self.client.budget.be_subtransactions)
