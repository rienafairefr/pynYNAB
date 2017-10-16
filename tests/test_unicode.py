# coding=utf-8
import unittest

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.schema import Payee
from tests.common_mock import MockConnection


class UnitTestsUnicode(unittest.TestCase):

    def test_8bitbytestringserror(self):
        # edge case
        # unicode failure scottrobertson #55
        payee = Payee(name='Caffè Nero')

        factory = nYnabClientFactory()

        client = factory.create_client(budget_name='budgetname', nynabconnection = MockConnection(),sync=False)

        client.budget.be_payees.append(payee)

        client.session.commit()
