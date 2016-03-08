
csvimport.py
------------
.. code-block:: bash

    usage: csvimport.py [-h] [--email Email] [--password Password]
                        [--level LoggingLevel] [--schema schemaName]
                        CSVpath BudgetName [AccountName]
    
    Manually import a CSV into a nYNAB budget Args that start with '--' (eg.
    --email) can also be set in a config file
    (C:\Users\Matthieu\AppData\Local\pynYNAB\pynYNAB\ynab.conf or ). The
    recognized syntax for setting (key, value) pairs is based on the INI and YAML
    formats (e.g. key=value or foo=TRUE). For full documentation of the
    differences from the standards please refer to the ConfigArgParse
    documentation. If an arg is specified in more than one place, then commandline
    values override config file values which override defaults.
    
    positional arguments:
      CSVpath               The CSV file to import
      BudgetName            The nYNAB budget to use (creates it if it doesnt exist
      AccountName           The nYNAB account name to use (default: None)
    
    optional arguments:
      -h, --help            show this help message and exit
      --email Email         The Email User ID for nYNAB (default: None)
      --password Password   The Password for nYNAB (default: None)
      --level LoggingLevel  Logging Level (default: None)
      --schema schemaName   The CSV schema to use (see csv_schemas directory)
                            (default: None)

migrate.py
----------
.. code-block:: bash

    usage: migrate.py [-h] [--email Email] [--password Password]
                      [--level LoggingLevel] [--budgetname BudgetName]
                      BudgetPath
    
    Migrate a YNAB4 budget transaction history to nYNAB, using pyynab Args that
    start with '--' (eg. --email) can also be set in a config file
    (C:\Users\Matthieu\AppData\Local\pynYNAB\pynYNAB\ynab.conf or ). The
    recognized syntax for setting (key, value) pairs is based on the INI and YAML
    formats (e.g. key=value or foo=TRUE). For full documentation of the
    differences from the standards please refer to the ConfigArgParse
    documentation. If an arg is specified in more than one place, then commandline
    values override config file values which override defaults.
    
    positional arguments:
      BudgetPath            The budget .ynab4 directory
    
    optional arguments:
      -h, --help            show this help message and exit
      --email Email         The Email User ID for nYNAB (default: None)
      --password Password   The Password for nYNAB (default: None)
      --level LoggingLevel  Logging Level (default: None)
      --budgetname BudgetName
                            Migrate to a differently named budget (default: None)

ofximport.py
------------
.. code-block:: bash

    usage: ofximport.py [-h] [--email Email] [--password Password]
                        [--level LoggingLevel]
                        OFXPath BudgetName
    
    Manually import an OFX into a nYNAB budget Args that start with '--' (eg.
    --email) can also be set in a config file
    (C:\Users\Matthieu\AppData\Local\pynYNAB\pynYNAB\ynab.conf or ). The
    recognized syntax for setting (key, value) pairs is based on the INI and YAML
    formats (e.g. key=value or foo=TRUE). For full documentation of the
    differences from the standards please refer to the ConfigArgParse
    documentation. If an arg is specified in more than one place, then commandline
    values override config file values which override defaults.
    
    positional arguments:
      OFXPath               The OFX file to import
      BudgetName            The nYNAB budget to use (creates it if it doesnt exist
    
    optional arguments:
      -h, --help            show this help message and exit
      --email Email         The Email User ID for nYNAB (default: None)
      --password Password   The Password for nYNAB (default: None)
      --level LoggingLevel  Logging Level (default: None)
