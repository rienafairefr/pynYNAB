.. image:: https://travis-ci.org/rienafairefr/pynYNAB.svg?branch=master
    :target: https://travis-ci.org/rienafairefr/pynYNAB

.. image:: https://coveralls.io/repos/github/rienafairefr/pynYNAB/badge.svg?branch=master
    :target: https://coveralls.io/github/rienafairefr/pynYNAB?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/pynYNAB


========
nYNABapi
========

a python client for the new YNAB API

Installation
------------

.. code-block:: bash

    $ pip install pynYNAB

Or you can download the source, then call `python setup.py install`

Usage
-----

Either code your own script that uses the pynYNAB api, or use the provided scripts, ofximport, YNAB4 migrate, csvimport

Scripts Documentation
---------------------

See appropriate `README`_

API Documentation
-----------------

See the wiki `WIKI`_ for an extended explanation and usage examples

Preventing harm to nYnab servers
---------------------------

I've taken all precautionary steps so that this python Client can't affect YNAB even if used too widely. 

* It honors requests by the server to throttle its requests  >  Same mechanisme that the JS app uses
* It self-limits the requests to 5 request per second 
* It clearly identifies itself by User-Agent > Easy to lock it out if it causes trouble

.. _README: https://github.com/rienafairefr/nYNABapi/blob/master/scripts/README.rst
.. _WIKI: https://github.com/rienafairefr/pynYNAB/wiki
