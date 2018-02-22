import csv
import logging
import os
import sys
from collections import namedtuple
from datetime import datetime

from pynYNAB.ClientFactory import clientfromargs
from pynYNAB.schema.budget import Payee, Transaction

scriptsdir = os.path.dirname(os.path.abspath(__file__))
schemas_dir = os.path.join(scriptsdir, 'csv_schemas')

LOG = logging.getLogger(__name__)


def verify_csvimport(schema, accountname=None):
    if 'account' not in schema.headers and accountname is None:
        LOG.error('schema headers: %s' % schema.headers)
        LOG.error('This schema does not have an account column and no account name was provided')
        exit(-1)


class CsvImportArgs(object):
    def __init__(self, csv_file, schema, account_name=None, import_duplicates=False):
        self.csv_file = csv_file
        self.schema = schema
        self.account_name = account_name
        self.import_duplicates = import_duplicates


def do_csvimport(args, client):
    LOG.debug('selected schema %s' % (args.schema,))

    LOG.debug('schema headers %s' % args.schema.headers)
    delta = 0

    accounts = {x.account_name: x for x in client.budget.accounts}
    payees = {p.name: p for p in client.budget.payees}
    mastercategories_perid = {m.id: m for m in client.budget.master_categories}
    subcategories = {}
    for s in client.budget.subcategories:
        m = mastercategories_perid[s.entities_master_category_id]
        subcategories[m.name + ':' + s.name] = s

    def getaccount(account_name):
        try:
            LOG.debug('searching for account %s' % account_name)
            return accounts[account_name]
        except KeyError:
            LOG.error('Couldn''t find this account: %s' % account_name)
            exit(-1)

    def getpayee(payee_name):
        global delta
        try:
            LOG.debug('searching for payee %s' % payee_name)
            return payees[payee_name]
        except KeyError:
            LOG.debug('Couldn''t find this payee: %s' % payee_name)
            payee = Payee(name=payee_name)
            client.budget.payees.append(payee)
            delta += 1
            return payee

    def getsubcategory(category_name):
        try:
            LOG.debug('searching for subcategory %s' % category_name)
            return subcategories[category_name]
        except KeyError:
            LOG.debug('Couldn''t find this category: %s' % category_name)
            exit(-1)

    entities_account_id = None
    if 'account' not in args.schema.headers:
        entities_account_id = getaccount(args.account_name).id

    amount = None
    if 'inflow' in args.schema.headers and 'outflow' in args.schema.headers:
        pass
    elif 'amount' in args.schema.headers:
        pass
    else:
        LOG.error('This schema doesn''t provide an amount column or (inflow,outflow) columns')
        exit(-1)

    csvrow = namedtuple('CSVrow', field_names=args.schema.headers)

    imported_date = datetime.now().date()

    LOG.debug('OK starting the import from %s ' % os.path.abspath(args.csv_file))
    with open(args.csv_file, 'r') as inputfile:
        header = []
        for i in range(0, args.schema.nheaders):
            header.append(inputfile.readline())
        for row in csv.reader(inputfile):
            if sys.version[0] == '2':
                row = [cell.decode('utf-8') for cell in row]
            if all(map(lambda x: x.strip() == '', row)):
                continue
            LOG.debug('read line %s' % row)
            result = csvrow(*list(args.schema.convert_row(*row, fail_fast=True)))
            if 'account' in args.schema.headers:
                entities_account_id = getaccount(result.account).id
            if entities_account_id is None:
                LOG.error(
                    'No account id, the account %s in the an account column was not recognized' % result.account)
                exit(-1)
            if 'inflow' in args.schema.headers and 'outflow' in args.schema.headers:
                amount = result.inflow - result.outflow
            elif 'amount' in args.schema.headers:
                amount = result.amount

            if 'category' in args.schema.headers and result.category:
                entities_subcategory_id = getsubcategory(result.category).id
            else:
                entities_subcategory_id = None
            if 'payee' in args.schema.headers:
                imported_payee = result.payee
            else:
                imported_payee = ''
            entities_payee_id = getpayee(imported_payee).id
            if 'memo' in args.schema.headers:
                memo = result.memo
            else:
                memo = ''

            transaction = Transaction(
                entities_account_id=entities_account_id,
                cash_amount=amount,
                amount=amount,
                date=result.date,
                entities_payee_id=entities_payee_id,
                entities_subcategory_id=entities_subcategory_id,
                imported_date=imported_date,
                imported_payee=imported_payee,
                memo=memo,
                source="Imported"
            )

            if args.import_duplicates or not (transaction.key2 in [tr.key2 for tr in client.budget.transactions]):
                LOG.debug('Appending transaction %s ' % transaction.get_dict())
                client.budget.transactions.append(transaction)
                delta += 1
            else:
                LOG.debug('Duplicate transaction found %s ' % transaction.get_dict())

    return delta
