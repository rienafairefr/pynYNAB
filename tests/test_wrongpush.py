import pytest

from pynYNAB.exceptions import WrongPushException
from pynYNAB.schema.budget import Transaction
from .common_mock import client


def test_wrong_push(client):
    client.budget.transactions.append(Transaction())
    client.budget.transactions.append(Transaction())
    pytest.raises(WrongPushException, lambda: client.push(expected_delta=1))


__all__ = ['client']
