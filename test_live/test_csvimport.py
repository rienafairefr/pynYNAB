import json
import os
from datetime import datetime
from tempfile import gettempdir

import configargparse

from pynYNAB.Entity import ComplexEncoder
from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.csvimport import do_csvimport
from test_live.common_Live import commonLive
from test_live.test_live import needs_account


class TestCsv(commonLive):
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
        args.csvfile = os.path.join(gettempdir(),'data.csv')
        args.accountname = None
        args.import_duplicates = False
        args.logginglevel = 'debug'

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Credit
"""
        with open(args.csvfile, mode='w') as f:
            f.writelines(content)

        transaction=self.getTr(datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants', 'Credit')

        for i in range(2):
            do_csvimport(args)
            self.reload()
            identical=[tr2 for tr2 in self.client.budget.be_transactions if transaction._hash() == tr2._hash()]
            print('Transactions with same hash: %s'%len(identical))
            self.assertTrue(len(identical) == 1)

    @needs_account('Cash')
    def test_duplicateForced(self):
        parser = configargparse.getArgumentParser('pynYNAB')
        args = parser.parse_known_args()[0]
        args.schema = 'example'
        args.csvfile = os.path.join(gettempdir(),'data.csv')
        args.accountname = None
        args.import_duplicates = True
        args.logginglevel = 'debug'

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
"""
        with open(args.csvfile, mode='w') as f:
            f.writelines(content)

        transaction=self.getTr(datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants', 'Cash')

        do_csvimport(args)
        self.reload()
        do_csvimport(args)
        self.reload()
        self.assertTrue(len([tr2 for tr2 in self.client.budget.be_transactions if transaction._hash() == tr2._hash()]) == 2)

    @needs_account('Cash')
    @needs_account('Checking Account')
    @needs_account('Savings')
    def test_import(self):
        parser = configargparse.getArgumentParser('pynYNAB')
        args = parser.parse_known_args()[0]
        args.schema = 'example'
        args.csvfile = os.path.join(gettempdir(),'data.csv')
        args.accountname = None
        args.import_duplicates=False
        args.logginglevel = 'debug'

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
2016-02-02,Thai Restaurant,-10,Food,Checking Account
2016-02-03,,10,Saving!,Savings
        """
        with open(args.csvfile, mode='w') as f:
            f.writelines(content)

        Transactions = [
            self.getTr(datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants', 'Cash'),
            self.getTr(datetime(year=2016, month=2, day=2).date(), 'Thai Restaurant', -10, 'Food', 'Checking Account'),
            self.getTr(datetime(year=2016, month=2, day=3).date(), '', 10, 'Saving!', 'Savings'),
        ]

        do_csvimport(args)
        self.reload()
        for tr in Transactions:
            print(json.dumps(tr, cls=ComplexEncoder))
            print(json.dumps(
                [tr2 for tr2 in self.client.budget.be_transactions if tr2.amount == tr.amount],
                cls=ComplexEncoder))
            self.assertTrue(self.client.budget.be_transactions.containsduplicate(tr))
