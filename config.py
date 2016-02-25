import logging

from appdirs import AppDirs
import os

appdir=AppDirs('nYNABpyClient')
try:
    os.makedirs(appdir.user_data_dir)
except:
    pass

cwd=os.path.dirname(__file__)

import configparser
cp = configparser.ConfigParser()
cp.read(os.path.join(cwd,"ynab.conf"))
email = cp.get('AUTHENTICATION', 'email',fallback=None)
password = cp.get('AUTHENTICATION', 'password',fallback=None)

if email is None or password is None:
    print('Please create or modify ynab.conf according to the format in ynab.conf.format')
    exit(-1)

logginglevel=cp.get('LOGGING','level',fallback='ERROR').upper()
logger=logging.getLogger('pynYNAB')
logging.basicConfig()
logger.setLevel(logginglevel)