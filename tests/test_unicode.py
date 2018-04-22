# coding=utf-8
import unittest

import pytest
import six

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.schema import Payee
from .common_mock import MockConnection


def run_test(payee_name):
    payee = Payee(name=payee_name)
    client = nYnabClientFactory().create_client(budget_name=u'budgetname',
                                                connection=MockConnection(),
                                                sync=False)
    client.budget.payees.append(payee)
    client.session.commit()


def test_8bitbytestringserror():
    # edge case unicode failure scottrobertson #55
    # if passing non-unicode strings this will fail
    run_test(u'Caffè Nero')
    # without the u fails in python 2.7
    if six.PY2:
        pytest.raises(Exception, lambda: run_test('Caffè Nero'))
