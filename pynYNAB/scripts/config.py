import logging
import os

from appdirs import AppDirs

LOG = logging.getLogger(__name__)

configfile = 'ynab.conf'
if not os.path.exists(configfile):
    myAppdir = AppDirs('pynYNAB').user_config_dir
    configfile = os.path.join(myAppdir, configfile)


def verify_common_args(args):
    if args.email is None:
        get_logger().error('No email user ID provided, please specify it at the command line or in %s' % (configfile,))
        exit(-1)
    if args.password is None:
        get_logger().error('No password provided, please specify it at the command line or in %s' % (configfile,))
        exit(-1)
    if args.budgetname is None:
        get_logger().error('No budget name provided, please specify it at the command line or in %s' % (configfile,))
        exit(-1)


def alert_quit_badconfig():
    print('Please modify ynab.conf situated in %s' % myAppdir)
    import shutil

    shutil.copy('ynab.conf.format', os.path.join(myAppdir, 'ynab.conf'))
    exit(-1)
