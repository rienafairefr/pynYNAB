# coding=utf-8
import unittest

import six

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.schema import Payee
from .common_mock import MockConnection


class UnitTestsUnicode(unittest.TestCase):
    def run_test(self, payee_name):
        payee = Payee(name=payee_name)
        client = nYnabClientFactory().create_client(budget_name=u'budgetname',
                                                    connection=MockConnection(),
                                                    sync=False)
        client.budget.payees.append(payee)
        client.session.commit()

    def test_8bitbytestringserror(self):
        # edge case unicode failure scottrobertson #55
        # if passing non-unicode strings this will fail
        self.run_test(u'Caffè Nero')
        # without the u fails in python 2.7
        if six.PY2:
            self.assertRaises(Exception, lambda:self.run_test('Caffè Nero'))
