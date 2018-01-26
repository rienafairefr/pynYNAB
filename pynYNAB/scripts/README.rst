
------------
.. code-block:: 
    usage: generate_doc.py [-h] [--email Email] [--password Password]
                           [--budget_name BudgetName] [--import-duplicates]
                           CSVpath schemaName [AccountName]
    
    Manually import a CSV into a nYNAB budget
    
    positional arguments:
      CSVpath               The CSV file to import
      schemaName            The CSV schema to use (see csv_schemas directory)
      AccountName           The nYNAB account name to use
    
    optional arguments:
      -h, --help            show this help message and exit
      --email Email         The Email User ID for nYNAB
      --password Password   The Password for nYNAB
      --budgetname BudgetName
                            The nYNAB budget to use
      -import-duplicates    Forces the import even if a duplicate (same date,
                            account, amount, memo, payee) is found

ofximport.py
------------
.. code-block:: 
    usage: generate_doc.py [-h] [--email Email] [--password Password]
                           [--budget_name BudgetName]
                           OFXPath
    
    Manually import an OFX into a nYNAB budget
    
    positional arguments:
      OFXPath               The OFX file to import
    
    optional arguments:
      -h, --help            show this help message and exit
      --email Email         The Email User ID for nYNAB
      --password Password   The Password for nYNAB
      --budget_name BudgetName
                            The nYNAB budget to use


Command Line / Config File Arguments
====================================
Args that start with '--' (eg. --email) can also be set in the config file
(ynab.yaml, or its path passed by --config parameter).
The recognized syntax for setting (key, value) pairs is based
on YAML format (key: value).
If an arg is specified in more than one
place, then commandline values override config file values.


