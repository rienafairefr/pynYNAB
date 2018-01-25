import argparse
import inspect
import json
import os
from getpass import getpass
import logging
import sys

import yaml
from jsontableschema import schema
from jsontableschema.exceptions import InvalidSchemaError
from jsontableschema.model import SchemaModel
from ofxtools import OFXTree

from pynYNAB.ClientFactory import clientfromargs, nYnabClientFactory, clientfromkwargs
from pynYNAB.scripts.csvimport import do_csvimport, verify_csvimport, schemas_dir
from pynYNAB.scripts.helpers import ConfigEnvArgumentParser
from pynYNAB.scripts.ofximport import do_ofximport

logging.basicConfig()

LOG = logging.getLogger(__name__)

parser = ConfigEnvArgumentParser('pynYNAB', add_help=False)

parser.add_argument('--email', metavar='Email', type=str, required=False,
                    help='The Email User ID for nYNAB', default=os.environ.get('NYNAB_EMAIL'))
parser.add_argument('--password', metavar='Password', type=str, required=False,
                    help='**insecure** The Password for nYNAB, omit it to enter it securely in a prompt',
                    default=os.environ.get('NYNAB_PASSWORD'))
parser.add_argument('--budget_name', metavar='BudgetName', type=str, required=False,
                    help='The nYNAB budget to use',
                    default=os.environ.get('NYNAB_BUDGETNAME'))


def valid_file(input):
    if not os.path.exists(input):
        raise argparse.ArgumentTypeError('file %s does not exist' % input)
    return input


def valid_schema(schema):
    if os.path.exists(schema):
        schemafile = schema + '.json'
    else:
        schemafile = os.path.join(schemas_dir, schema + '.json')

    if not os.path.exists(schemafile):
        msg = 'This schema file %s doesn''t exist in current directory or csv_schemas directory'% (schema+'.json')
        raise argparse.ArgumentTypeError(msg)

    try:
        schema = SchemaModel(schemafile, case_insensitive_headers=True)

        with open(schemafile, 'r') as sf:
            schemacontent = json.load(sf)
            try:
                setattr(schema, 'nheaders', schemacontent['nheaders'])
            except KeyError:
                setattr(schema, 'nheaders', 1)
        return schema

    except InvalidSchemaError as e:
        raise argparse.ArgumentTypeError('Invalid CSV schema %s' % e)


class CsvImport(object):
    @property
    def parser(self):
        csv_parser = ConfigEnvArgumentParser(parents=[parser])
        csv_parser.description = inspect.getdoc(self.command)
        csv_parser.add_argument('csvfile', metavar='CSVpath', type=valid_file,
                                help='The CSV file to import')
        csv_parser.add_argument('schema', metavar='schemaName', type=str,
                                help='The CSV schema to use (see csv_schemas directory)')
        csv_parser.add_argument('accountname', metavar='AccountName', type=str, nargs='?',
                                help='The nYNAB account name  to use')
        csv_parser.add_argument('--force-duplicates', action='store_true',
                                help='Forces the import even if a duplicate (same date, account, amount, memo, payee) is found')
        return csv_parser

    def command(self):
        """Manually import a CSV into a nYNAB budget"""
        print('pynYNAB CSV import')

        args = self.parser.parse_args()
        verify_common_args(args)

        verify_csvimport(args.schema, args.accountname)
        client = clientfromkwargs(**args)
        delta = do_csvimport(args, client)
        client.push(expected_delta=delta)


class OfxImport(object):
    @property
    def parser(self):
        ofx_parser = ConfigEnvArgumentParser(parents=[parser], add_help=False)
        ofx_parser.description = inspect.getdoc(self.command)
        ofx_parser.add_argument('file', metavar='OFXPath', type=valid_file,
                                help='The OFX file to import')
        return ofx_parser

    def command(self):
        """Manually import an OFX into a nYNAB budget"""
        print('pynYNAB OFX import')

        args = self.parser.parse_args()
        verify_common_args(args)

        client = clientfromkwargs(**args)
        delta = do_ofximport(args.file, client)
        client.push(expected_delta=delta)


COMMANDS = dict(csvimport=CsvImport,
                ofximport=OfxImport)


class MainCommands(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='nYnab-CLI using the python library',
            usage='''nynab <command> [<args>]

            ''')

        parser.add_argument('command', help='Subcommand to run', choices=COMMANDS.keys())
        parser.usage += 'commands : ' + ','.join(COMMANDS.keys())
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])

        if args.command not in COMMANDS:
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        if getattr(args, 'password', None):
            args.password = getpass('YNAB password:')


        sys.argv.pop(1)

        COMMANDS[args.command]().command()


def verify_common_args(args):
    if args.email is None:
        LOG.error('No email user ID provided, please specify it '
                  'at the command line or in a YAML config file passed through --config')
        exit(-1)
    if args.password is None:
        LOG.error('No password provided, please specify it '
                  'at the command line or in a YAML config file passed through --config')
        exit(-1)
    if args.budget_name is None:
        LOG.error('No budget name provided, please specify it '
                  'at the command line or in a YAML config file passed through --config')
        exit(-1)


def main():
    MainCommands()
