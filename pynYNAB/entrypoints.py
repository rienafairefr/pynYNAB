import inspect
import os

import configargparse

from pynYNAB.Client import clientfromargs
from pynYNAB.scripts.config import verify_common_args, get_logger, configfile
from pynYNAB.scripts.csvimport import do_csvimport
from pynYNAB.scripts.ofximport import do_ofximport


def csvimport_main():
    print('pynYNAB CSV import')
    """Manually import a CSV into a nYNAB budget"""
    parser = configargparse.getArgumentParser('pynYNAB')
    parser.description = inspect.getdoc(csvimport_main)
    parser.add_argument('csvfile', metavar='CSVpath', type=str,
                        help='The CSV file to import')
    parser.add_argument('schema', metavar='schemaName', type=str,
                        help='The CSV schema to use (see csv_schemas directory)')
    parser.add_argument('accountname', metavar='AccountName', type=str, nargs='?',
                        help='The nYNAB account name  to use')
    parser.add_argument('-import-duplicates', action='store_true',
                        help='Forces the import even if a duplicate (same date, account, amount, memo, payee) is found')

    args = parser.parse_args()
    verify_common_args(args)

    if not os.path.exists(args.csvfile):
        get_logger().error('input CSV file does not exist')
        exit(-1)

    client = clientfromargs(args)
    delta = do_csvimport(args,client)
    client.push(expected_delta=delta)

def ofximport_main():
    print('pynYNAB OFX import')
    """Manually import an OFX into a nYNAB budget"""

    parser = configargparse.getArgumentParser('pynYNAB')
    parser.description = inspect.getdoc(ofximport_main)
    parser.add_argument('ofxfile', metavar='OFXPath', type=str,
                        help='The OFX file to import')

    args = parser.parse_args()
    verify_common_args(args)
    client = clientfromargs(args)
    delta = do_ofximport(args,client)
    client.push(expected_delta=delta)


parser = configargparse.getArgumentParser('pynYNAB', default_config_files=[configfile],
                                          add_env_var_help=True,
                                          add_config_file_help=True,
                                          auto_env_var_prefix='NYNAB_')

parser.add_argument('--email', metavar='Email', type=str, required=False,
                    help='The Email User ID for nYNAB')
parser.add_argument('--password', metavar='Password', type=str, required=False,
                    help='The Password for nYNAB')
parser.add_argument('--budgetname', metavar='BudgetName', type=str, required=False,
                    help='The nYNAB budget to use')