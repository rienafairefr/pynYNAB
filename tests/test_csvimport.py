import os
from datetime import datetime

import configargparse

from pynYNAB.Entity import ComplexEncoder
from pynYNAB.budget import Transaction
from pynYNAB.scripts.csvimport import do_csvimport
from tests.common_Live import commonLive
import json

class Test_CSV(commonLive):


    def test_import(self):
        parser = configargparse.getArgumentParser('pynYNAB')
        args=parser.parse_known_args()[0]
        args.schema = 'example'
        args.csvfile = os.path.join('data', 'test.csv')
        args.accountname = None
        args.level= 'debug'

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
2016-02-02,Thai Restaurant,-10,Food,Checking Account
2016-02-03,,10,Saving!,Savings
        """
        with open(args.csvfile, mode='w') as f:
            f.writelines(content)
        imported_date=datetime.now().date()
        def getTr(date,payee,amount,memo,account):
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
        Transactions = [
            getTr(datetime(year=2016, month=2, day=1).date(),'Super Pants Inc.',-20,'Buying pants','Cash'),
            getTr(datetime(year=2016, month=2, day=2).date(),'Thai Restaurant',-10,'Food','Checking Account'),
            getTr(datetime(year=2016, month=2, day=3).date(),'',10,'Saving!','Savings'),
        ]

        do_csvimport(args)
        self.reload()
        transactionshashes= {tr.hash():tr for tr in self.client.budget.be_transactions}
        for tr in Transactions:

            print(json.dumps(tr,cls=ComplexEncoder))
            print(json.dumps([tr2 for tr2 in self.client.budget.be_transactions if tr2.amount==tr.amount and tr2.memo == tr.memo],cls=ComplexEncoder))
            self.assertIn(tr.hash(),transactionshashes)
