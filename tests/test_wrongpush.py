import pytest

from pynYNAB.exceptions import WrongPushException
from pynYNAB.schema.budget import Transaction
from .common_mock import client


def test_wrong_push(client):
    client.budget.be_transactions.append(Transaction())
    client.budget.be_transactions.append(Transaction())
    pytest.raises(WrongPushException, lambda: client.push(expected_delta=1))


__all__ = ['client']
