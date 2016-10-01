import argparse
import logging
import os
from appdirs import AppDirs
import configargparse

configfile = 'ynab.conf'
if not os.path.exists(configfile):
    myAppdir = AppDirs('pynYNAB').user_config_dir
    configfile = os.path.join(myAppdir, configfile)



parser = configargparse.getArgumentParser('pynYNAB',default_config_files=[configfile],
                                          add_env_var_help=True,
                                          add_config_file_help=True,
                                          auto_env_var_prefix='NYNAB_')
parser.add_argument('--email', metavar='Email', type=str, required=False,
                    help='The Email User ID for nYNAB')
parser.add_argument('--password', metavar='Password', type=str, required=False,
                    help='The Password for nYNAB')
parser.add_argument('--logginglevel', metavar='LoggingLevel', type=str.lower, required=False,default='error',
                    choices=['critical','error','warn','warning','info','debug'],
                    help='Logging Level')

parser.add_argument('--budgetname', metavar='BudgetName', type=str, required=False,
                        help='The nYNAB budget to use')


def get_logger(args=None):
    args = parser.parse_known_args()[0] if args is None else args
    logginglevel = args.logginglevel.upper()
    logger = logging.getLogger('pynYNAB')
    logging.basicConfig()
    logger.setLevel(logginglevel)
    return logger


def test_common_args(args):
    if args.email is None:
        get_logger().error('No email user ID provided, please specify it at the command line or in %s'%(configfile,))
        exit(-1)
    if args.password is None:
        get_logger().error('No password provided, please specify it at the command line or in %s'%(configfile,))
        exit(-1)
    if args.budgetname is None:
        get_logger().error('No budget name provided, please specify it at the command line or in %s'%(configfile,))
        exit(-1)

def alert_quit_badconfig():
    print('Please modify ynab.conf situated in %s' % myAppdir)
    import shutil

    shutil.copy('ynab.conf.format', os.path.join(myAppdir, 'ynab.conf'))
    exit(-1)
