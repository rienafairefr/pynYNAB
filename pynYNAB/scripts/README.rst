
csvimport.py
------------
.. code-block:: 

    usage: csvimport.py [-h] [--email Email] [--password Password]
                        [--level LoggingLevel] [--budgetname BudgetName]
                        CSVpath schemaName [AccountName]
    
    Manually import a CSV into a nYNAB budget
    
    positional arguments:
      CSVpath               The CSV file to import
      schemaName            The CSV schema to use (see csv_schemas directory)
      AccountName           The nYNAB account name to use (default: None)
    
    optional arguments:
      -h, --help            show this help message and exit
    
    command line or config file arguments:
      --email Email         The Email User ID for nYNAB (default: None)
      --password Password   The Password for nYNAB (default: None)
      --level LoggingLevel  Logging Level (default: error)
      --budgetname BudgetName
                            The nYNAB budget to use (default: None)

migrate.py
----------
.. code-block:: 

    usage: migrate.py [-h] [--email Email] [--password Password]
                      [--level LoggingLevel] [--budgetname BudgetName]
                      BudgetPath
    
    Migrate a YNAB4 budget transaction history to nYNAB, using pyynab
    
    positional arguments:
      BudgetPath            The budget .ynab4 directory
    
    optional arguments:
      -h, --help            show this help message and exit
    
    command line or config file arguments:
      --email Email         The Email User ID for nYNAB (default: None)
      --password Password   The Password for nYNAB (default: None)
      --level LoggingLevel  Logging Level (default: error)
      --budgetname BudgetName
                            The nYNAB budget to use (default: None)

ofximport.py
------------
.. code-block:: 

    usage: ofximport.py [-h] [--email Email] [--password Password]
                        [--level LoggingLevel] [--budgetname BudgetName]
                        OFXPath
    
    Manually import an OFX into a nYNAB budget
    
    positional arguments:
      OFXPath               The OFX file to import
    
    optional arguments:
      -h, --help            show this help message and exit
    
    command line or config file arguments:
      --email Email         The Email User ID for nYNAB (default: None)
      --password Password   The Password for nYNAB (default: None)
      --level LoggingLevel  Logging Level (default: error)
      --budgetname BudgetName
                            The nYNAB budget to use (default: None)

Command Line / Config File Arguments
====================================
Args that start with '--' (eg. --email) can also be set in the config file
(ynab.conf). The recognized syntax for setting (key, value) pairs is based
on the INI and YAML formats (e.g. key=value or foo=TRUE). For full
documentation of the differences from the standards please refer to the
ConfigArgParse documentation. If an arg is specified in more than one
place, then commandline values override config file values.
