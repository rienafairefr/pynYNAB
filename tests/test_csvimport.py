import os
import random
from datetime import datetime

import configargparse

from pynYNAB.Entity import AccountTypes
from pynYNAB.budget import Account, Transaction, Payee
from pynYNAB.scripts.csvimport import do_csvimport
from tests.test_live import liveTests


class Test_CSV(liveTests):
    def util_get_empty_account_by_name_if_doesnt_exist(self, name):
        accounts = {a.account_name: a for a in self.client.budget.be_accounts if
                    a.account_name == name and not a.is_tombstone}
        if name in accounts:
            account=accounts[name]
            self.client.delete_account(account)
            self.reload()

            accounts = {a.account_name: a for a in self.client.budget.be_accounts if
                    a.account_name == name and not a.is_tombstone}

            self.assertTrue(name not in accounts)

        account = Account(
            account_type=random.choice(list(AccountTypes)),
            account_name=name
        )

        self.client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())
        self.reload()
        self.assertIn(account, self.client.budget.be_accounts)
        return account

    def util_add_payee_by_name_if_doesnt_exist(self, name):
        payees = {p.name: p for p in self.client.budget.be_payees if
                    p.name == name and not p.is_tombstone}
        if name in payees:
            return payees[name]
        payee = Payee(
            name=name
        )

        self.client.budget.be_payees.append(payee)
        self.client.sync()
        self.reload()
        self.assertIn(payee, self.client.budget.be_payees)
        return payee

    def test_import(self):
        parser = configargparse.getArgumentParser('pynYNAB')
        args=parser.parse_known_args()[0]
        args.schema = 'example'
        args.csvfile = os.path.join('data', 'test.csv')
        args.accountname = None

        content = """Date,Payee,Amount,Memo,Account
2016-02-01,Super Pants Inc.,-20,Buying pants,Cash
2016-02-02,Thai Restaurant,-10,Food,Checking Account
2016-02-03,,10,Saving!,Savings
        """
        with open(args.csvfile, mode='w') as f:
            f.writelines(content)

        Transactions = [
            Transaction(
                entities_account_id=self.util_get_empty_account_by_name_if_doesnt_exist('Cash').id,
                date=datetime(year=2016, month=2, day=1),
                entities_payee_id=self.util_add_payee_by_name_if_doesnt_exist('Super Pants Inc.').id,
                memo='Buying pants',
                amount=-20
            ),
            Transaction(
                entities_account_id=self.util_get_empty_account_by_name_if_doesnt_exist('Checking Account').id,
                date=datetime(year=2016, month=2, day=2),
                entities_payee_id=self.util_add_payee_by_name_if_doesnt_exist('Thai Restaurant').id,
                memo='Food',
                amount=-10
            ),
            Transaction(
                entities_account_id=self.util_get_empty_account_by_name_if_doesnt_exist('Cash').id,
                date=datetime(year=2016, month=2, day=3),
                entities_payee_id=self.util_add_payee_by_name_if_doesnt_exist('').id,
                memo='Saving!',
                amount=10
            )
        ]

        do_csvimport(args)
        self.reload()

        self.assertTrue(all(tr in self.client.budget.be_transactions for tr in Transactions))
