import configargparse
import inspect
from datetime import datetime
from ofxtools import OFXTree

from pynYNAB.Client import clientfromargs
from pynYNAB.schema.budget import Transaction, Payee
from pynYNAB.scripts.config import test_common_args


def ofximport_main():
    print('pynYNAB OFX import')
    """Manually import an OFX into a nYNAB budget"""

    parser = configargparse.getArgumentParser('pynYNAB')
    parser.description = inspect.getdoc(ofximport_main)
    parser.add_argument('ofxfile', metavar='OFXPath', type=str,
                        help='The OFX file to import')

    args = parser.parse_args()
    test_common_args(args)
    do_ofximport(args)

def do_ofximport(args, client = None):
    if client is None:
        client = clientfromargs(args)

    tree = OFXTree()
    tree.parse(args.ofxfile)
    response = tree.convert()
    stmts = response.statements

    accounts = client.budget.be_accounts
    accountvsnotes={account.note:account for account in accounts if account.note is not None}

    for stmt in stmts:
        key = stmt.account.bankid + ' ' + stmt.account.branchid + ' ' + stmt.account.acctid
        if all(key not in note for note in accountvsnotes):
            if len(accounts) == 0:
                print('No accounts available in this budget')
                exit(-1)

            # ask user input for which bank account this is, then save it into the account note in nYNAB
            account = client.select_account_ui()

            # Save the selection in the nYNAB account note
            addon = 'key[' + key + ']key'
            if account.note is not None:
                account.note += addon
            else:
                account.note = addon
            client.budget.be_accounts.modify(account)
            client.sync()
        else:
            for note in accountvsnotes:
                if key in note:
                    account=accountvsnotes[note]

                    imported_date=datetime.now().date()

                    for ofx_transaction in stmt.transactions:
                        payee_name = ofx_transaction.name if ofx_transaction.payee is None else ofx_transaction.payee
                        try:
                            payee = next(p for p in client.budget.be_payees if p.name == payee_name)
                        except StopIteration:
                            payee=Payee(
                                name=payee_name
                            )
                            client.budget.be_payees.append(payee)
                            client.sync()

                        # use ftid so we don't import duplicates
                        if not any(ofx_transaction.fitid in transaction.memo for transaction in client.budget.be_transactions if
                                   transaction.memo is not None and transaction.entities_account_id == account.id):

                            transaction = Transaction(
                                date=ofx_transaction.dtposted,
                                memo=ofx_transaction.memo + '    '+ofx_transaction.fitid,
                                imported_payee=payee_name,
                                entities_payee_id=payee.id,
                                imported_date=imported_date,
                                source="Imported",
                                check_number=ofx_transaction.checknum,
                                amount=float(ofx_transaction.trnamt),
                                entities_account_id=account.id
                            )
                            client.add_transaction(transaction)

if __name__ == "__main__":
    ofximport_main()