========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/pynynab/badge/?style=flat
    :target: https://readthedocs.org/projects/pynynab
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/rienafairefr/pynYNAB.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/rienafairefr/pynYNAB

.. |coveralls| image:: https://coveralls.io/repos/rienafairefr/pynYNAB/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/rienafairefr/pynYNAB

.. |version| image:: https://img.shields.io/pypi/v/pynYNAB.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pynYNAB

.. |commits-since| image:: https://img.shields.io/github/commits-since/rienafairefr/pynYNAB/v0.5.5.svg
    :alt: Commits since latest release
    :target: https://github.com/rienafairefr/pynYNAB/compare/v0.5.5...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/pynYNAB.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pynYNAB

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pynYNAB.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pynYNAB

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pynYNAB.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pynYNAB


.. end-badges

a python client for the new YNAB API

* Free software: MIT license

Installation
============

::

    pip install pynYNAB

Documentation
=============

https://pynYNAB.readthedocs.io/

Usage
-----

Either code your own script that uses the pynYNAB api, or use the provided scripts, ofximport, YNAB4 migrate, csvimport

API Documentation
-----------------

See the wiki `WIKI`_ for an extended explanation and usage examples

Preventing harm to nYnab servers
--------------------------------

I've taken all precautionary steps so that this python Client can't affect YNAB even if used too widely.

* It honors requests by the server to throttle its requests  >  Same mechanisme that the JS app uses
* It self-limits the requests to 5 request per second
* It clearly identifies itself by User-Agent > Easy to lock it out if it causes trouble

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

.. _WIKI: https://github.com/rienafairefr/pynYNAB/wiki
