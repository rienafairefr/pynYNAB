import os
from appdirs import AppDirs
import configargparse
from pynYNAB.log import logger

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


def test_common_args(args):
    if args.email is None:
        logger.error('No email user ID provided, please specify it at the command line or in %s'%(configfile,))
        exit(-1)
    if args.password is None:
        logger.error('No password provided, please specify it at the command line or in %s'%(configfile,))
        exit(-1)
    if args.budgetname is None:
        logger.error('No budget name provided, please specify it at the command line or in %s'%(configfile,))
        exit(-1)

def alert_quit_badconfig():
    print('Please modify ynab.conf situated in %s' % myAppdir)
    import shutil

    shutil.copy('ynab.conf.format', os.path.join(myAppdir, 'ynab.conf'))
    exit(-1)
