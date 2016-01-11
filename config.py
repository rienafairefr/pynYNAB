from appdirs import AppDirs
import os

appdir=AppDirs('nYNABpyClient')
try:
    os.makedirs(appdir.user_data_dir)
except:
    pass