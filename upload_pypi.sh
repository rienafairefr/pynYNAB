#!/bin/bash
if [[ "${TRAVIS_TAG}" != "" ]]; then

rm -rf dist

python setup.py sdist bdist_wheel
python ynab-api/setup.py sdist bdist_wheel

twine upload -u $PYPI_USER -p $PYPI_PASSWORD dist/*

fi;