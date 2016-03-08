import argparse
import logging
import os
from appdirs import AppDirs
import configargparse

myAppdir = AppDirs('pynYNAB').user_config_dir
configfile=os.path.join(myAppdir, 'ynab.conf')

parser = configargparse.getArgumentParser('pynYNAB',default_config_files=[configfile],add_config_file_help=False)
group=parser.add_argument_group('command line or config file arguments')
group.add_argument('--email', metavar='Email', type=str, required=False,
                    help='The Email User ID for nYNAB')
group.add_argument('--password', metavar='Password', type=str, required=False,
                    help='The Password for nYNAB')
group.add_argument('--level', metavar='LoggingLevel', type=str.lower, required=False,default='error',
                    choices=['critical','error','warn','warning','info','debug'],
                    help='Logging Level')

group.add_argument('--budgetname', metavar='BudgetName', type=str, required=False,
                        help='The nYNAB budget to use')


def get_logger():
    args=parser.parse_known_args()[0]
    logginglevel = args.level.upper()
    logger = logging.getLogger('pynYNAB')
    logging.basicConfig()
    logger.setLevel(logginglevel)
    return logging


def alert_quit_badconfig():
    print('Please modify ynab.conf situated in %s' % myAppdir)
    import shutil

    shutil.copy('ynab.conf.format', os.path.join(myAppdir, 'ynab.conf'))
    exit(-1)
