import json
import os
import tempfile
import unittest
from datetime import datetime

import configargparse

from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.ofximport import do_ofximport
from pynYNAB.utils import get_or_create_account, get_or_create_payee
from tests.common_mock import TestCommonMock


class TestOFX(TestCommonMock):
    def testiimport(self):
        parser = configargparse.getArgumentParser('pynYNAB')
        args = parser.parse_known_args()[0]
        args.ofxfile = os.path.join(tempfile.gettempdir(), 'data.ofx')
        args.logginglevel = 'debug'

        content = """OFXHEADER:100
DATA:OFXSGML
VERSION:102
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE
<OFX>
    <SIGNONMSGSRSV1>
    <SONRS>
        <STATUS>
            <CODE>0
            <SEVERITY>INFO
        </STATUS>
        <DTSERVER>20130313133728
        <LANGUAGE>FRA
    </SONRS>
    </SIGNONMSGSRSV1>
    <BANKMSGSRSV1>
        <STMTTRNRS>
            <TRNUID>29939615002
            <STATUS>
                <CODE>0
                <SEVERITY>INFO
            </STATUS>
            <STMTRS>
                <CURDEF>EUR
                    <BANKACCTFROM>
                    <BANKID>11706
                    <BRANCHID>41029
                    <ACCTID>29939615002
                    <ACCTTYPE>CHECKING
                </BANKACCTFROM>
                <BANKTRANLIST>
                    <DTSTART>20130128000000
                    <DTEND>20130314235959
                    <STMTTRN>
                        <TRNTYPE>CHECK
                        <DTPOSTED>20130312
                        <TRNAMT>-491.09
                        <FITID>13071099780237330004
                        <CHECKNUM>0003445
                        <NAME>CHEQUE
                        <MEMO>CHEQUE
                    </STMTTRN>
                </BANKTRANLIST>
                <LEDGERBAL>
                    <BALAMT>-6348.01
                    <DTASOF>20130312
                </LEDGERBAL>
                <AVAILBAL>
                <BALAMT>-6348.01
                <DTASOF>20130312
                </AVAILBAL>
            </STMTRS>
        </STMTTRNRS>
    </BANKMSGSRSV1>
</OFX>"""
        with open(args.ofxfile, 'w') as f:
            f.writelines(content)
        imported_date = datetime.now().date()

        testaccount = 'TEST'

        account = get_or_create_account(self.client,testaccount)

        key = '11706 41029 29939615002'
        account.note = 'great note key[%s]key' % key

        payee = get_or_create_payee(self.client,'CHEQUE')
        amount = -491.09

        transaction = Transaction(
            entities_account=account,
            date=datetime(year=2013, month=3, day=12).date(),
            entities_payee=payee,
            imported_payee=payee,
            source='Imported',
            check_number='0003445',
            memo='CHEQUE    13071099780237330004',
            amount=amount,
            credit_amount=0,
            imported_date=imported_date
        )

        delta = do_ofximport(args,self.client)
        self.assertEqual(delta,1,msg="should add exactly one transaction")
        self.assertIn(transaction.key2, [tr.key2 for tr in self.client.budget.be_transactions],
                      msg='couldnt find an imported transaction after ofx import')
