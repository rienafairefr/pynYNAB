# coding=utf-8

from pynYNAB.Client import nYnabClient
from pynYNAB.config import email, password
from pynYNAB.connection import nYnabConnection


if __name__ == "__main__":
    connection = nYnabConnection(email, password)
    nYNABobject = nYnabClient(connection, budget_name='My Budget')

    # TODO list accounts, transactions, etc in the main ?

