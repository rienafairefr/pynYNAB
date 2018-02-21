import logging
from datetime import datetime

from ofxtools import OFXTree

from pynYNAB.schema.budget import Transaction, Payee

LOG = logging.getLogger(__name__)


def get_stmts(ofxfile):
    tree = OFXTree()
    tree.parse(ofxfile)
    response = tree.convert()
    return response.statements


def do_ofximport(file, client):
    delta = 0
    stmts = get_stmts(file)

    accounts = client.budget.accounts
    accountvsnotes = {account.note: account for account in accounts if account.note is not None}

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
        else:
            for note in accountvsnotes:
                if key in note:
                    account = accountvsnotes[note]

                    imported_date = datetime.now().date()

                    for ofx_transaction in stmt.transactions:
                        payee_name = ofx_transaction.name if ofx_transaction.payee is None else ofx_transaction.payee
                        try:
                            payee = next(p for p in client.budget.payees if p.name == payee_name)
                        except StopIteration:
                            payee = Payee(
                                name=payee_name
                            )
                            client.budget.payees.append(payee)
                            delta += 1

                        # use ftid so we don't import duplicates
                        if not any(ofx_transaction.fitid in transaction.memo for transaction in
                                   client.budget.transactions if
                                   transaction.memo is not None and transaction.entities_account_id == account.id):
                            transaction = Transaction(
                                date=ofx_transaction.dtposted,
                                memo=ofx_transaction.memo + '    ' + ofx_transaction.fitid,
                                imported_payee=payee_name,
                                entities_payee_id=payee.id,
                                imported_date=imported_date,
                                source="Imported",
                                check_number=ofx_transaction.checknum,
                                amount=float(ofx_transaction.trnamt),
                                entities_account_id=account.id
                            )
                            client.budget.transactions.append(transaction)
                            delta += 1

    return delta
