import unittest

from NYnabConnection import NYnabConnection
from budget import Transaction
from config import email, password
from nYNAB import NYnab


class Test1(unittest.TestCase):
    def setUp(self):
        self.connection = NYnabConnection(email, password, reload=True)
        self.nYNABobject = NYnab(self.connection, reload=True)

    def test_addtransaction(self):
        from datetime import datetime
        budget=self.nYNABobject.budget
        for acc in budget.be_accounts:
            if not acc.is_tombstone:
                transaction=Transaction(
                    accepted=True,
                    amount=1000,
                    cash_amount=0,
                    cleared='Uncleared',
                    date=datetime.now().strftime('%Y-%m-%d'),
                    credit_amount=0,
                    entities_account_id=acc.id,
                    entities_payee_id=None,
                    entities_subcategory_id=None,
                    is_tombstone=False
                )
                budget.be_transactions.append(transaction)

                self.nYNABobject.sync()
                self.nYNABobject = NYnab(self.connection, reload=True)

                self.assertIn(transaction,self.nYNABobject.budget.be_transactions)
                return
        raise ValueError('No available account !')

    def test_deletetransaction(self):
        from datetime import datetime
        budget=self.nYNABobject.budget
        for acc in budget.be_accounts:
            if not acc.is_tombstone:
                for transaction in budget.be_transactions:
                    if transaction.entities_account_id == acc.id and not transaction.is_tombstone:

                        budget.be_transactions.delete(transaction)
                        self.nYNABobject.sync()

                        self.nYNABobject = NYnab(self.connection, reload=True)

                        resulttransaction=self.nYNABobject.budget.be_transactions.get(transaction.id)
                        self.assertTrue( resulttransaction is None or resulttransaction.is_tombstone==True)
                        return
                raise ValueError('No available transaction in this account !')
        raise ValueError('No available account !')



