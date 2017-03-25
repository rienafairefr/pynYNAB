import json
import os
import unittest
from datetime import datetime
from tempfile import gettempdir

import configargparse

from pynYNAB.Client import nYnabClient
from pynYNAB.schema.Entity import ComplexEncoder
from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.csvimport import do_csvimport
from test_live.common import CommonLive, needs_account


class TestCsv(unittest.TestCase):
    def SetUp(self):
        self.client = nYnabClient()

    def getTr(self, date, payee, amount, memo, account):
        imported_date = datetime.now().date()
        return Transaction(
            entities_account_id=self.util_get_empty_account_by_name_if_doesnt_exist(account).id,
            date=date,
            entities_payee_id=self.util_add_payee_by_name_if_doesnt_exist(payee).id,
            imported_payee=payee,
            source='Imported',
            memo=memo,
            amount=amount,
            cash_amount=amount,
            imported_date=imported_date
        )

    @needs_account('Credit')
    def test_duplicate(self):
        parser = configargparse.getArgumentParser('pynYNAB')
        args = parser.parse_known_args()[0]
        args.schema = 'example'
        args.csvfile = os.path.join(gettempdir(), 'data.csv')
        args.accountname = None
        args.import_duplicates = False
        args.logginglevel = 'debug'

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Credit
"""
        with open(args.csvfile, mode='w') as f:
            f.writelines(content)

        transaction = self.getTr(datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants',
                                 'Credit')
        self.client.budget.be_transactions.append(transaction)
        delta = do_csvimport(args, self.client)
        self.assertEqual(delta, 0)

    @needs_account('Cash')
    def test_duplicateForced(self):
        parser = configargparse.getArgumentParser('pynYNAB')
        args = parser.parse_known_args()[0]
        args.schema = 'example'
        args.csvfile = os.path.join(gettempdir(), 'data.csv')
        args.accountname = None
        args.import_duplicates = True
        args.logginglevel = 'debug'

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
"""
        with open(args.csvfile, mode='w') as f:
            f.writelines(content)

        transaction = self.getTr(datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants',
                                 'Cash')

        self.client.budget.be_transactions.append(transaction)
        delta = do_csvimport(args)
        self.assertEqual(delta, 1)
        self.assertEqual(self.client.budget.be_transactions.count(transaction), 2)

    @needs_account('Cash')
    @needs_account('Checking Account')
    @needs_account('Savings')
    def test_import(self):
        parser = configargparse.getArgumentParser('pynYNAB')
        args = parser.parse_known_args()[0]
        args.schema = 'example'
        args.csvfile = os.path.join(gettempdir(), 'data.csv')
        args.accountname = None
        args.import_duplicates = False
        args.logginglevel = 'debug'

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
2016-02-02,Thai Restaurant,-10,Food,Checking Account
2016-02-03,,10,Saving!,Savings
        """
        with open(args.csvfile, mode='w') as f:
            f.writelines(content)

        transactions = [
            self.getTr(datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants', 'Cash'),
            self.getTr(datetime(year=2016, month=2, day=2).date(), 'Thai Restaurant', -10, 'Food', 'Checking Account'),
            self.getTr(datetime(year=2016, month=2, day=3).date(), '', 10, 'Saving!', 'Savings'),
        ]

        do_csvimport(args)
        for transaction in transactions:
            self.assertIn(transaction, self.client.budget.be_transactions)
