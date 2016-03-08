import codecs
import inspect
from collections import namedtuple
from datetime import datetime
import configargparse
import os

import sys
from jsontableschema.model import SchemaModel

def csvimport_main():
    """Manually import a CSV into a nYNAB budget"""

    from pynYNAB.Client import nYnabClient
    from pynYNAB.budget import Transaction, Payee
    from pynYNAB.config import get_logger
    from pynYNAB.connection import nYnabConnection

    parser = configargparse.getArgumentParser('pynYNAB')
    parser.description=inspect.getdoc(csvimport_main)
    parser.add_argument('csvfile', metavar='CSVpath', type=str,
                        help='The CSV file to import')
    parser.add_argument('schema', metavar='schemaName', type=str,
                        help='The CSV schema to use (see csv_schemas directory)')
    parser.add_argument('accountname', metavar='AccountName', type=str,
                        help='The nYNAB account name  to use')

    args = parser.parse_known_args()[0]

    if not os.path.exists(args.csvfile):
        get_logger().ERROR('input CSV file does not exist')
        exit(-1)

    connection = nYnabConnection(args.email, args.password)
    schemas_dir = 'csv_schemas'
    client = nYnabClient(connection, budget_name=args.budgetname)

    if os.path.exists(args.schema):
        schemafile = args.schema
    else:
        schemafile = os.path.join(schemas_dir, args.schema + '.json')
        if not os.path.exists(schemafile):
            get_logger().ERROR('This schema doesn''t exist in csv_schemas')
            exit(-1)
    schema = SchemaModel(schemafile, case_insensitive_headers=True)

    if 'account' not in schema.headers and args.accountname is None:
        get_logger().error('This schema does not have an account column and no account name was provided')
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
            return accounts[accountname]
        except KeyError:
            get_logger().error('Couldn''t find this account: %s' % accountname)
            exit(-1)


    def getpayee(payeename):
        try:
            return payees[payeename]
        except KeyError:
            get_logger().debug('Couldn''t find this payee: %s' % payeename)
            payee=Payee(name=payeename)
            client.budget.be_payees.append(payee)
            return payee


    def getsubcategory(categoryname):
        try:
            return subcategories[categoryname]
        except KeyError:
            get_logger().debug('Couldn''t find this category: %s' % categoryname)
            exit(-1)


    if 'account' not in schema.headers:
        entities_account_id = getaccount(args.accountname).id

    if 'inflow' in schema.headers and 'outflow' in schema.headers:
        def amountfun(result): return result.inflow - result.outflow
    elif 'amount' in schema.headers:
        def amountfun(result): return result.amount
    else:
        get_logger().error('This schema doesn''t provide an amount column or (inflow,outflow) columns')
        exit(-1)

    Row = namedtuple('CSVrow', field_names=schema.headers)
    transactions = []



    imported_date=datetime.now().date()

    existing_transactions_hashes={tr.hash():tr for tr in client.budget.be_transactions if not tr.is_tombstone}

    with codecs.open(args.csvfile, 'r', encoding='utf-8') as inputfile:
        inputfile.readline()
        for row in inputfile.readlines():
            row = row.strip().split(',')
            result = Row(*list(schema.convert_row(*row, fail_fast=True)))
            if 'account' in schema.headers:
                entities_account_id = getaccount(result.account).id
            if 'inflow' in schema.headers and 'outflow' in schema.headers:
                amount = result.inflow - result.outflow
            elif 'amount' in schema.headers:
                amout = result.amount
            else:
                get_logger().error('Couldn''t find this account: %s' % args.accountname)
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
            if transaction.hash() not in existing_transactions_hashes:
                transactions.append(transaction)


    client.add_transactions(transactions)

if __name__ == "__main__":
    sys.exit(csvimport_main())