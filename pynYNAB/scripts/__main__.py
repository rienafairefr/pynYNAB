import argparse
import inspect
import os
from getpass import getpass

import configargparse
import logging

import sys
from appdirs import AppDirs

from pynYNAB.ClientFactory import clientfromargs
from pynYNAB.scripts.csvimport import do_csvimport, verify_csvimport
from pynYNAB.scripts.ofximport import do_ofximport, verify_ofximport

logging.basicConfig()

configfile = 'ynab.conf'
if not os.path.exists(configfile):
    myAppdir = AppDirs('pynYNAB').user_config_dir
    configfile = os.path.join(myAppdir, configfile)

LOG = logging.getLogger(__name__)

parser = configargparse.getArgumentParser('pynYNAB', default_config_files=[configfile],
                                          add_env_var_help=True,
                                          add_config_file_help=True,
                                          auto_env_var_prefix='NYNAB_')

parser.add_argument('--email', metavar='Email', type=str, required=False,
                    help='The Email User ID for nYNAB')
parser.add_argument('--password', metavar='Password', type=str, required=False,
                    help='**insecure** The Password for nYNAB, just omit it to enter it securely in a prompt')
parser.add_argument('--budgetname', metavar='BudgetName', type=str, required=False,
                    help='The nYNAB budget to use')


class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)


class MainCommands(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='nYnab-CLI using the python API',
            usage='''nynab <command> [<args>]

            ''')
        argcommands = parser.add_argument('command', help='Subcommand to run',choices=['csvimport','ofximport'])
        parser.usage += 'commands : '+','.join(argcommands.choices)
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        if getattr(args, 'password', None):
            args.password = getpass('YNAB password:')
        sys.argv.pop(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    @classproperty
    def csvimport_parser(cls):
        csv_parser = argparse.ArgumentParser(parents=[parser],add_help=False)
        csv_parser.description = inspect.getdoc(cls.csvimport)
        csv_parser.add_argument('csvfile', metavar='CSVpath', type=str,
                                      help='The CSV file to import')
        csv_parser.add_argument('schema', metavar='schemaName', type=str,
                                      help='The CSV schema to use (see csv_schemas directory)')
        csv_parser.add_argument('accountname', metavar='AccountName', type=str, nargs='?',
                                      help='The nYNAB account name  to use')
        csv_parser.add_argument('-import-duplicates', action='store_true',
                                      help='Forces the import even if a duplicate (same date, account, amount, memo, payee) is found')
        return csv_parser

    @classmethod
    def csvimport(cls):
        """Manually import a CSV into a nYNAB budget"""
        print('pynYNAB CSV import')

        args = cls.csvimport_parser.parse_args()
        verify_common_args(args)

        schema = verify_csvimport(args)
        client = clientfromargs(args)
        delta = do_csvimport(args, schema, client)
        client.push(expected_delta=delta)

    @classproperty
    def ofximport_parser(cls):
        ofx_parser = argparse.ArgumentParser(parents=[parser],add_help=False)
        ofx_parser.description = inspect.getdoc(cls.ofximport)
        ofx_parser.add_argument('ofxfile', metavar='OFXPath', type=str,
                            help='The OFX file to import')
        return ofx_parser

    @classmethod
    def ofximport(cls):
        """Manually import an OFX into a nYNAB budget"""
        print('pynYNAB OFX import')

        args = cls.ofximport_parser.parse_args()
        verify_common_args(args)

        stmts = verify_ofximport(args)
        client = clientfromargs(args)
        delta = do_ofximport(args, stmts, client)
        client.push(expected_delta=delta)


def verify_common_args(args):
    if args.email is None:
        LOG.error('No email user ID provided, please specify it at the command line or in %s' % (configfile,))
        exit(-1)
    if args.password is None:
        LOG.error('No password provided, please specify it at the command line or in %s' % (configfile,))
        exit(-1)
    if args.budgetname is None:
        LOG.error('No budget name provided, please specify it at the command line or in %s' % (configfile,))
        exit(-1)


def main():
    MainCommands()
