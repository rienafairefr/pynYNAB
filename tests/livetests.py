import random
import unittest
from datetime import datetime, timedelta
from functools import wraps
import configargparse

from pynYNAB import KeyGenerator
from pynYNAB.Client import nYnabClient
from pynYNAB.Entity import AccountTypes
from pynYNAB.budget import Transaction, Account, Subtransaction
from pynYNAB.connection import nYnabConnection


class liveTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(liveTests, self).__init__(*args, **kwargs)
        self.account = None
        self.budet = None
        self.transaction = None
        self.client = None

    def setUp(self):
        parser=configargparse.getArgumentParser('pynYNAB')
        args=parser.parse_known_args()[0]
        connection = nYnabConnection(args.email, args.password)
        self.client = nYnabClient(connection, budget_name='My Budget')

    def needs_account(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            for account in self.client.budget.be_accounts:
                if not account.is_tombstone:
                    self.account = account
                    fn(self, *args, **kwargs)
                    return
            raise ValueError('No available account !')

        return wrapped

    def needs_transaction(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            for transaction in self.client.budget.be_transactions:
                if transaction.entities_account_id == self.account.id and not transaction.is_tombstone:
                    self.transaction = transaction
                    fn(self, *args, **kwargs)
                    return
            raise ValueError('No available transaction !')

        return wrapped

    def test_add_account_alltypes(self):
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

            self.setUp()

            self.assertIn(account, self.client.budget.be_accounts)

    @needs_account
    def test_deleteaccount(self):
        self.client.delete_account(self.account)
        self.setUp()

        result = self.client.budget.be_transactions.get(self.account.id)
        self.assertTrue(result is None or result.is_tombstone == True)
        return

    @needs_account
    def test_addtransaction(self):
        from datetime import datetime
        transaction = Transaction(
            amount=1,
            cleared='Uncleared',
            date=datetime.now(),
            entities_account_id=self.account.id,
        )
        self.client.add_transaction(transaction)

        self.setUp()

        self.assertIn(transaction, self.client.budget.be_transactions)
        return

    @needs_account
    def test_addtransactions(self):
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

        self.setUp()
        for transaction in transactions:
            self.assertIn(transaction, self.client.budget.be_transactions)

    @needs_account
    @needs_transaction
    def test_deletetransaction(self):
        self.client.delete_transaction(self.transaction)
        self.setUp()

        resulttransaction = self.client.budget.be_transactions.get(self.transaction.id)
        self.assertTrue(resulttransaction is None or resulttransaction.is_tombstone == True)

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

        self.setUp()

        self.assertIn(transaction, self.client.budget.be_transactions)
        self.assertIn(sub1, self.client.budget.be_subtransactions)
        self.assertIn(sub2, self.client.budget.be_subtransactions)

    @needs_account
    @needs_transaction
    def test_split(self):
        subcat1, subcat2 = tuple(random.sample(self.client.budget.be_subcategories, 2))
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

        self.setUp()

        self.assertIn(sub1, self.client.budget.be_subtransactions)
        self.assertIn(self.transaction, self.client.budget.be_transactions)
        self.assertIn(sub2, self.client.budget.be_subtransactions)
