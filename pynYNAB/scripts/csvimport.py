import csv
import json
import logging
import os
import sys
from collections import namedtuple
from datetime import datetime

from jsontableschema.exceptions import InvalidSchemaError
from jsontableschema.model import SchemaModel

from pynYNAB.ClientFactory import clientfromargs
from pynYNAB.schema.budget import Payee, Transaction

scriptsdir = os.path.dirname(os.path.abspath(__file__))
schemas_dir = os.path.join(scriptsdir, 'csv_schemas')

LOG = logging.getLogger(__name__)


def verify_csvimport(args):
    if not os.path.exists(args.csvfile):
        LOG.error('input CSV file %s does not exist'% args.csvfile)
        exit(-1)

    if os.path.exists(args.schema):
        schemafile = args.schema + '.json'
    else:
        schemafile = os.path.join(schemas_dir, args.schema + '.json')
    if not os.path.exists(schemafile):
        LOG.error('This schema file %s doesn''t exist in current directory or csv_schemas directory'% (args.schema+'.json'))
        exit(-1)

    try:
        schema = SchemaModel(schemafile, case_insensitive_headers=True)

        if 'account' not in schema.headers and args.accountname is None:
            LOG.error('schema headers: %s'%schema.headers)
            LOG.error('This schema does not have an account column and no account name was provided')
            exit(-1)

        with open(schemafile, 'r') as sf:
            schemacontent = json.load(sf)
            try:
                setattr(schema, 'nheaders', schemacontent['nheaders'])
            except KeyError:
                setattr(schema, 'nheaders', 1)


        return schema

    except InvalidSchemaError as e:
        LOG.error('Invalid CSV schema %s'%e)
        exit(-1)




def do_csvimport(args, schema, client=None):
    if client is None:
        client = clientfromargs(args)

    LOG.debug('selected schema %s' % (args.schema,))

    LOG.debug('schema headers %s' % schema.headers)
    delta = 0

    accounts = {x.account_name: x for x in client.budget.be_accounts}
    payees = {p.name: p for p in client.budget.be_payees}
    mastercategories_perid = {m.id: m for m in client.budget.be_master_categories}
    subcategories = {}
    for s in client.budget.be_subcategories:
        m = mastercategories_perid[s.entities_master_category_id]
        subcategories[m.name + ':' + s.name] = s

    def getaccount(accountname):
        try:
            LOG.debug('searching for account %s' % accountname)
            return accounts[accountname]
        except KeyError:
            LOG.error('Couldn''t find this account: %s' % accountname)
            exit(-1)

    def getpayee(payeename):
        global delta
        try:
            LOG.debug('searching for payee %s' % payeename)
            return payees[payeename]
        except KeyError:
            LOG.debug('Couldn''t find this payee: %s' % payeename)
            payee = Payee(name=payeename)
            client.budget.be_payees.append(payee)
            delta += 1
            return payee

    def getsubcategory(categoryname):
        try:
            LOG.debug('searching for subcategory %s' % categoryname)
            return subcategories[categoryname]
        except KeyError:
            LOG.debug('Couldn''t find this category: %s' % categoryname)
            exit(-1)

    entities_account_id = None
    if 'account' not in schema.headers:
        entities_account_id = getaccount(args.accountname).id

    amount = None
    if 'inflow' in schema.headers and 'outflow' in schema.headers:
        pass
    elif 'amount' in schema.headers:
        pass
    else:
        LOG.error('This schema doesn''t provide an amount column or (inflow,outflow) columns')
        exit(-1)

    csvrow = namedtuple('CSVrow', field_names=schema.headers)

    imported_date = datetime.now().date()

    LOG.debug('OK starting the import from %s ' % os.path.abspath(args.csvfile))
    with open(args.csvfile, 'r') as inputfile:
        header = []
        for i in range(0, schema.nheaders):
            header.append(inputfile.readline())
        for row in csv.reader(inputfile):
            if sys.version[0] == '2':
                row = [cell.decode('utf-8') for cell in row]
            if all(map(lambda x: x.strip() == '', row)):
                continue
            LOG.debug('read line %s' % row)
            result = csvrow(*list(schema.convert_row(*row, fail_fast=True)))
            if 'account' in schema.headers:
                entities_account_id = getaccount(result.account).id
            if entities_account_id is None:
                LOG.error(
                    'No account id, the account %s in the an account column was not recognized' % result.account)
                exit(-1)
            if 'inflow' in schema.headers and 'outflow' in schema.headers:
                amount = result.inflow - result.outflow
            elif 'amount' in schema.headers:
                amount = result.amount

            if 'category' in schema.headers and result.category:
                entities_subcategory_id = getsubcategory(result.category).id
            else:
                entities_subcategory_id = None
            if 'payee' in schema.headers:
                imported_payee = result.payee
            else:
                imported_payee = ''
            entities_payee_id = getpayee(imported_payee).id
            if 'memo' in schema.headers:
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

            if args.import_duplicates or not (transaction.key2 in [tr.key2 for tr in client.budget.be_transactions]):
                LOG.debug('Appending transaction %s ' % transaction.get_dict())
                client.budget.be_transactions.append(transaction)
                delta += 1
            else:
                LOG.debug('Duplicate transaction found %s ' % transaction.get_dict())

    return delta


if __name__ == "__main__":
    from pynYNAB.scripts.__main__ import MainCommands
    MainCommands.csvimport()
