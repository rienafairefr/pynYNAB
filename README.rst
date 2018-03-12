.. image:: https://travis-ci.org/rienafairefr/pynYNAB.svg?branch=master
    :target: https://travis-ci.org/rienafairefr/pynYNAB

.. image:: https://coveralls.io/repos/github/rienafairefr/pynYNAB/badge.svg?branch=master
    :target: https://coveralls.io/github/rienafairefr/pynYNAB?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/pynYNAB


========
nYNABapi
========

a python client for the new YNAB API. This is integrating with the old-school, internal-use API
on https://app.youneedabudget.com/api/v1, not the new API that went live on December 2017

Installation
------------

.. code-block:: bash

    $ pip install pynYNAB

Or you can download the source, then call `python setup.py install`

Usage
-----

For more in-depth info about the library, go to the documentation `DOCS`_

Either code your own script that uses the pynYNAB api, or use the provided scripts, `ynab ofximport`,  or `ynab csvimport`

Scripts Documentation
---------------------

Using these scripts you can import a bunch of transactions in your budget, using either a CSV or an OFX file
This is especially useful if your bank is not supported by the automatic import feature of YNAB

See more documentation at `SCRIPTS_DOCS`_

API Documentation
-----------------

See some extended explanation in the `WIKI`_ or the `DOCS`_

Preventing harm to YNAB servers
--------------------------------

I've taken all precautionary steps so that this python Client can't affect YNAB even if used too widely.

* It honors requests by the server to throttle its requests  >  Same mechanisme that the JS app uses
* It self-limits the requests to 5 request per second 
* It clearly identifies itself by User-Agent > Easy to lock it out if it causes trouble

.. _README: https://github.com/rienafairefr/nYNABapi/blob/master/scripts/README.rst
.. _WIKI: https://github.com/rienafairefr/pynYNAB/wiki
.. _DOCS: http://rienafairefr.github.io/pynYNAB/
.. _SCRIPTS_DOCS: http://rienafairefr.github.io/pynYNAB/scripts.html