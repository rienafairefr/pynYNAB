import codecs
import inspect
from collections import namedtuple
from datetime import datetime
import configargparse
import os

from jsontableschema.model import SchemaModel

from pynYNAB.Client import clientfromargs
from pynYNAB.budget import Payee, Transaction
from pynYNAB.config import get_logger, test_common_args

scriptsdir=os.path.dirname(os.path.abspath(__file__))
schemas_dir = os.path.join(scriptsdir,'csv_schemas')

def csvimport_main():
    print('pynYNAB CSV import')
    """Manually import a CSV into a nYNAB budget"""
    parser = configargparse.getArgumentParser('pynYNAB')
    parser.description=inspect.getdoc(csvimport_main)
    parser.add_argument('csvfile', metavar='CSVpath', type=str,
                        help='The CSV file to import')
    parser.add_argument('schema', metavar='schemaName', type=str,
                        help='The CSV schema to use (see csv_schemas directory)')
    parser.add_argument('accountname', metavar='AccountName', type=str,nargs='?',
                        help='The nYNAB account name  to use')
    parser.add_argument('-import-duplicates', metavar='importduplicates', action='store_true',
                        help='Forces the import even if a duplicate (same date, account, amount, memo, payee) is found')

    args = parser.parse_args()
    test_common_args(args)

    if not os.path.exists(args.csvfile):
        get_logger().error('input CSV file does not exist')
        exit(-1)

    do_csvimport(args)


def do_csvimport(args):
    client = clientfromargs(args)

    get_logger(args).debug('selected schema %s' % (args.schema,))
    if os.path.exists(args.schema):
        schemafile = args.schema
    else:
        schemafile = os.path.join(schemas_dir, args.schema + '.json')
        if not os.path.exists(schemafile):
            get_logger(args).error('This schema doesn''t exist in csv_schemas')
            exit(-1)
    schema = SchemaModel(schemafile, case_insensitive_headers=True)
    get_logger(args).debug('schema headers %s' % schema.headers)

    if 'account' not in schema.headers and args.accountname is None:
        get_logger(args).error('This schema does not have an account column and no account name was provided')
        exit(-1)

    accounts = {x.account_name: x for x in client.budget.be_accounts}
    payees = {p.name: p for p in client.budget.be_payees}
    mastercategories_perid = {m.id: m for m in client.budget.be_master_categories}
    subcategories = {}
    for s in client.budget.be_subcategories:
        m=mastercategories_perid[s.entities_master_category_id]
        subcategories[m.name+':'+s.name]=s

    def getaccount(accountname):
        try:
            get_logger(args).debug('searching for account %s' % accountname)
            return accounts[accountname]
        except KeyError:
            get_logger(args).error('Couldn''t find this account: %s' % accountname)
            exit(-1)

    def getpayee(payeename):
        try:
            get_logger(args).debug('searching for payee %s' % payeename)
            return payees[payeename]
        except KeyError:
            get_logger(args).debug('Couldn''t find this payee: %s' % payeename)
            payee=Payee(name=payeename)
            client.budget.be_payees.append(payee)
            return payee

    def getsubcategory(categoryname):
        try:
            get_logger(args).debug('searching for subcategory %s' % categoryname)
            return subcategories[categoryname]
        except KeyError:
            get_logger(args).debug('Couldn''t find this category: %s' % categoryname)
            exit(-1)

    if 'account' not in schema.headers:
        entities_account_id = getaccount(args.accountname).id

    if 'inflow' in schema.headers and 'outflow' in schema.headers:
        def amountfun(result): return result.inflow - result.outflow
    elif 'amount' in schema.headers:
        def amountfun(result): return result.amount
    else:
        get_logger(args).error('This schema doesn''t provide an amount column or (inflow,outflow) columns')
        exit(-1)

    csvrow = namedtuple('CSVrow', field_names=schema.headers)
    transactions = []

    imported_date=datetime.now().date()

    get_logger(args).debug('OK starting the import from %s '%os.path.abspath(args.csvfile))
    with codecs.open(args.csvfile, 'r', encoding='utf-8') as inputfile:
        inputfile.readline()
        for row in inputfile.readlines():
            get_logger(args).debug('read line %s' % row)
            if row.strip() == '':
                continue
            row = row.strip().split(',')
            result = csvrow(*list(schema.convert_row(*row, fail_fast=True)))
            if 'account' in schema.headers:
                entities_account_id = getaccount(result.account).id
            if 'inflow' in schema.headers and 'outflow' in schema.headers:
                amount = result.inflow - result.outflow
            elif 'amount' in schema.headers:
                amout = result.amount
            else:
                get_logger(args).error('Couldn''t find this account: %s' % args.accountname)
                exit(-1)

            if 'category' in schema.headers:
                entities_subcategory_id = getsubcategory(result.category).id
            else:
                entities_subcategory_id = None
            if 'payee' in schema.headers:
                imported_payee=result.payee
            else:
                imported_payee=''
            entities_payee_id = getpayee(imported_payee).id
            if 'memo' in schema.headers:
                memo=result.memo
            else:
                memo=''


            transaction=Transaction(
                entities_account_id=entities_account_id,
                amount=amountfun(result),
                date=result.date,
                entities_payee_id=entities_payee_id,
                entities_subcategory_id=entities_subcategory_id,
                imported_date=imported_date,
                imported_payee=imported_payee,
                memo=memo,
                source="Imported"
            )
            if args.importduplicates or (not client.budget.be_transactions.containsduplicate(transaction)):
                get_logger(args).debug('Appending transaction %s '%transaction.getdict())
                transactions.append(transaction)
            else:
                get_logger(args).debug('Duplicate transaction found %s '%transaction.getdict())



    client.add_transactions(transactions)

if __name__ == "__main__":
    csvimport_main()