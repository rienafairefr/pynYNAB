import json
import os
import tempfile
from datetime import datetime

import configargparse

from pynYNAB.Client import clientfromargs
from pynYNAB.Entity import ComplexEncoder
from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.ofximport import do_ofximport
from test_live.common_Live import commonLive


class TestOFX(commonLive):
    def testiimport(self):
        parser = configargparse.getArgumentParser('pynYNAB')
        args=parser.parse_known_args()[0]
        args.ofxfile = os.path.join(tempfile.gettempdir(),'data.ofx')
        args.logginglevel= 'debug'

        self.client=clientfromargs(args)

        content="""OFXHEADER:100
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
        with open(args.ofxfile,'w') as f:
            f.writelines(content)
        imported_date=datetime.now().date()

        testaccount='TEST'
        account=self.util_get_empty_account_by_name_if_doesnt_exist(testaccount)

        key = '11706 41029 29939615002'
        account.note='great note key[%s]key' %key
        self.client.budget.be_accounts.modify(account)
        self.client.sync()

        def getTr(date,payee,amount,memo,account):
            return Transaction(
                entities_account_id=account.id,
                date=date,
                entities_payee_id=self.util_add_payee_by_name_if_doesnt_exist(payee).id,
                imported_payee=payee,
                source='Imported',
                check_number='0003445',
                memo=memo,
                amount=amount,
                cash_amount=amount,
                imported_date=imported_date
            )
        Transactions = [
            getTr(datetime(year=2013, month=3, day=12).date(),'CHEQUE',-491.09,'CHEQUE    13071099780237330004',account),
        ]

        do_ofximport(args)
        self.reload()
        for tr in Transactions:
            print('Should have been imported:')
            print(json.dumps(tr,cls=ComplexEncoder))
            print('Found in the register:')
            print(json.dumps([tr2 for tr2 in self.client.budget.be_transactions if tr2.amount==tr.amount],cls=ComplexEncoder))
            self.assertTrue(self.client.budget.be_transactions.containsduplicate(tr),
                            msg='couldnt find a transaction with the same hash after ofx import')
