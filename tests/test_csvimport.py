import os
from datetime import datetime
from tempfile import gettempdir

from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.__main__ import valid_schema
from pynYNAB.scripts.csvimport import do_csvimport, verify_csvimport, CsvImportArgs
from pynYNAB.utils import get_or_create_account, get_or_create_payee
from test_live.common import needs_account
from .common_mock import TestCommonMock


class TestCsv(TestCommonMock):
    def getTr(self, date, payee, amount, memo, account):
        imported_date = datetime.now().date()
        return Transaction(
            entities_account_id=get_or_create_account(self.client, account).id,
            date=date,
            entities_payee_id=get_or_create_payee(self.client, payee).id,
            imported_payee=payee,
            source='Imported',
            memo=memo,
            amount=amount,
            cash_amount=amount,
            imported_date=imported_date
        )

    @needs_account('Credit')
    def test_duplicate(self):
        args = CsvImportArgs(os.path.join(gettempdir(), 'data.csv'), valid_schema('example'), None,
                             import_duplicates=False)

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Credit
"""
        with open(args.csv_file, mode='w') as f:
            f.writelines(content)

        transaction = self.getTr(datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants',
                                 'Credit')
        self.client.budget.transactions.append(transaction)
        schema = verify_csvimport(args.schema, args.account_name)
        delta = do_csvimport(args, self.client)
        self.assertEqual(delta, 0)

    @needs_account('Cash')
    def test_duplicateForced(self):
        args = CsvImportArgs(os.path.join(gettempdir(), 'data.csv'), valid_schema('example'), None, True)

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
"""
        with open(args.csv_file, mode='w') as f:
            f.writelines(content)

        transaction = self.getTr(datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants',
                                 'Cash')

        self.client.budget.transactions.append(transaction)
        schema = verify_csvimport(args.schema, args.account_name)
        delta = do_csvimport(args, self.client)
        self.assertEqual(delta, 1)

        self.assertEqual(sum(1 for tr in self.client.budget.transactions if tr.key2 == transaction.key2), 2)

    @needs_account('Cash')
    @needs_account('Checking Account')
    @needs_account('Savings')
    def test_import(self):
        args = CsvImportArgs(os.path.join(gettempdir(), 'data.csv'), valid_schema('example'), import_duplicates=False)

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
2016-02-02,Thai Restaurant,-10,Food,Checking Account
2016-02-03,,10,Saving!,Savings
        """
        with open(args.csv_file, mode='w') as f:
            f.writelines(content)

        transactions = [
            self.getTr(datetime(year=2016, month=2, day=1).date(), 'Super Pants Inc.', -20, 'Buying pants', 'Cash'),
            self.getTr(datetime(year=2016, month=2, day=2).date(), 'Thai Restaurant', -10, 'Food', 'Checking Account'),
            self.getTr(datetime(year=2016, month=2, day=3).date(), '', 10, 'Saving!', 'Savings'),
        ]

        schema = verify_csvimport(args.schema, args.account_name)
        do_csvimport(args, self.client)
        for transaction in transactions:
            self.assertIn(transaction.key2, [tr.key2 for tr in self.client.budget.transactions])
