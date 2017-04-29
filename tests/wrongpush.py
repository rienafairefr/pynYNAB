import unittest

from pynYNAB.Client import WrongPushException
from pynYNAB.schema.Client import nYnabClient_
from pynYNAB.schema.budget import Transaction


class TestWrongPush(unittest.TestCase):
    def TestWrongPush(self):
        client = nYnabClient_(budgetname='Test')
        client.budget.be_transactions.append(Transaction())
        client.budget.be_transactions.append(Transaction())
        self.assertRaises(WrongPushException,lambda: client.push(expected_delta=1))
