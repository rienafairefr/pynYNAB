import random
import unittest
from datetime import datetime, timedelta
from functools import wraps

import KeyGenerator
from Entity import AccountTypes
from NYnabConnection import nYnabConnection
from budget import Transaction, Account, Payee, Subtransaction
from config import email, password
from nYNAB import nYnab


class Live_tests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Live_tests, self).__init__(*args, **kwargs)
        self.account = None
        self.budet = None
        self.transaction = None
        self.nYNABobject = None

    def setUp(self):
        connection = nYnabConnection(email, password, reload=True)
        self.nYNABobject = nYnab(connection, budget_name='My Budget', reload=True)

    def needs_account(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            for account in self.nYNABobject.budget.be_accounts:
                if not account.is_tombstone:
                    self.account = account
                    fn(self, *args, **kwargs)
                    return
            raise ValueError('No available account !')

        return wrapped

    def needs_transaction(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            for transaction in self.nYNABobject.budget.be_transactions:
                if transaction.entities_account_id == self.account.id and not transaction.is_tombstone:
                    self.transaction = transaction
                    fn(self, *args, **kwargs)
                    return
            raise ValueError('No available transaction !')

        return wrapped

    def test_addaccount(self):
        account_type = AccountTypes.Checking
        account_name = KeyGenerator.generateUUID()
        budget = self.nYNABobject.budget

        for account in budget.be_accounts:
            if account.account_name == account_name:
                return
        sortable_index = max([account.sortable_index for account in budget.be_accounts])
        account = Account(
            account_type=account_type,
            account_name=account_name,
            sortable_index=sortable_index,
        )

        self.nYNABobject.add_account(account, balance=0, balance_date=datetime.now())

        self.nYNABobject.do_init(True)

        self.assertIn(account, self.nYNABobject.budget.be_accounts)

    @needs_account
    def test_deleteaccount(self):
        self.nYNABobject.delete_account(self.account)
        self.nYNABobject.do_init(True)

        result = self.nYNABobject.budget.be_transactions.get(self.account.id)
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
        self.nYNABobject.add_transaction(transaction)

        self.nYNABobject.do_init(True)

        self.assertIn(transaction, self.nYNABobject.budget.be_transactions)
        return

    @needs_account
    def test_addtransactions(self):
        from datetime import datetime

        transactions = []
        transactions.append(Transaction(
                amount=random.randint(-10, 10),
                cleared='Uncleared',
                date=datetime.now()-8*timedelta(days=365),
                entities_account_id=self.account.id,
            ))

        transactions.append(Transaction(
                amount=random.randint(-10, 10),
                cleared='Uncleared',
                date=datetime.now()+8*timedelta(days=365),
                entities_account_id=self.account.id,
            ))


        n = 3
        for i in range(len(transactions)-n):
            transactions.append(Transaction(
                amount=random.randint(-10, 10),
                cleared='Uncleared',
                date=datetime.now(),
                entities_account_id=self.account.id,
            ))
        self.nYNABobject.add_transactions(transactions)
        print('Time for request: ' + str(self.nYNABobject.connection.lastrequest_elapsed.total_seconds()) + ' s')

        self.nYNABobject.do_init(True)
        for transaction in transactions:
            self.assertIn(transaction, self.nYNABobject.budget.be_transactions)

    @needs_account
    @needs_transaction
    def test_deletetransaction(self):
        budget = self.nYNABobject.budget

        self.nYNABobject.delete_transaction(self.transaction)
        self.nYNABobject.do_init(True)

        resulttransaction = self.nYNABobject.budget.be_transactions.get(self.transaction.id)
        self.assertTrue(resulttransaction is None or resulttransaction.is_tombstone == True)

    @needs_account
    def test_add_splittransactions(self):
        subcatSplit_id = next(subcategory.id for subcategory in self.nYNABobject.budget.be_subcategories if
                              subcategory.internal_name == 'Category/__Split__')
        transaction = Transaction(
            amount=1,
            date=datetime.now(),
            entities_account_id=self.account.id,
            entities_subcategory_id=subcatSplit_id
        )
        sub1 = Subtransaction(
            amount=5000,
            entities_transaction_id=transaction.id
        )
        sub2 = Subtransaction(
            amount=5000,
            entities_transaction_id=transaction.id
        )
        self.nYNABobject.budget.be_transactions.append(transaction)
        self.nYNABobject.budget.be_subtransactions.append(sub1)
        self.nYNABobject.budget.be_subtransactions.append(sub2)

        self.nYNABobject.sync()

        self.nYNABobject.do_init(True)

        self.assertIn(transaction, self.nYNABobject.budget.be_transactions)
        self.assertIn(sub1, self.nYNABobject.budget.be_subtransactions)
        self.assertIn(sub2, self.nYNABobject.budget.be_subtransactions)

    @needs_account
    @needs_transaction
    def test_split(self):
        subcat1, subcat2 = tuple(random.sample(self.nYNABobject.budget.be_subcategories, 2))
        subcatSplit_id = next(subcategory.id for subcategory in self.nYNABobject.budget.be_subcategories if
                              subcategory.internal_name == 'Category/__Split__')
        self.transaction.entities_subcategory_id = subcatSplit_id

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

        self.nYNABobject.budget.be_subtransactions.append(sub1)
        self.nYNABobject.budget.be_subtransactions.append(sub2)
        self.nYNABobject.budget.be_transactions.modify(self.transaction)

        self.nYNABobject.sync()

        self.nYNABobject.do_init(True)

        self.assertIn(sub1, self.nYNABobject.budget.be_subtransactions)
        self.assertIn(self.transaction, self.nYNABobject.budget.be_transactions)
        self.assertIn(sub2, self.nYNABobject.budget.be_subtransactions)
