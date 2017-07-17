from pynYNAB.scripts.__main__ import MainCommands

with open('README.rst', 'w') as readme:


    module = 'csvimport.py'
    readme.writelines('\n'.join([module, '-' * len(module), '.. code-block:: ', '']))
    readme.writelines('    ' + line+'\r' for line in MainCommands.csvimport_parser.format_help().splitlines())

    readme.write('\n')
    module = 'ofximport.py'
    readme.writelines('\n'.join([module, '-' * len(module), '.. code-block:: ', '']))
    readme.writelines('    ' + line+'\r' for line in MainCommands.ofximport_parser.format_help().splitlines())

    readme.write('\n')

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
