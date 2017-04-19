import unittest

from pynYNAB.Client import nYnabClient
from pynYNAB.exceptions import WrongPushException
from pynYNAB.schema.budget import Transaction


class TestWrongPush(unittest.TestCase):
    def TestWrongPush(self):
        client = nYnabClient(budgetname='Test')
        client.budget.be_transactions.append(Transaction())
        client.budget.be_transactions.append(Transaction())
        self.assertRaises(WrongPushException,lambda: client.push(expected_delta=1))
