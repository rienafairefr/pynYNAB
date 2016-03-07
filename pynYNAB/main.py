# coding=utf-8

from Client import nYnabClient
from config import email, password
from connection import nYnabConnection


if __name__ == "__main__":
    connection = nYnabConnection(email, password)
    nYNABobject = nYnabClient(connection, budget_name='My Budget')

    # TODO list accounts, transactions, etc in the main ?

