import os
import subprocess

with open('README.rst', 'w') as readme:
    for module in os.listdir(os.path.dirname(__file__)):
        if module == os.path.basename(__file__) or module == '__init__.py' or module[-3:] != '.py':
            continue
        readme.write('\n')
        readme.writelines('\n'.join([module,'-'*len(module),'.. code-block:: ','']))
        process=subprocess.Popen([module,'-h'],shell=True,stdout=subprocess.PIPE)
        readme.write('\n')
        for line in process.stdout:
            readme.write('    '+line)

    readme.writelines("""
Command Line / Config File Arguments
====================================
Args that start with '--' (eg. --email) can also be set in the config file
(ynab.conf). The recognized syntax for setting (key, value) pairs is based
on the INI and YAML formats (e.g. key=value or foo=TRUE). For full
documentation of the differences from the standards please refer to the
ConfigArgParse documentation. If an arg is specified in more than one
place, then commandline values override config file values.
""")

