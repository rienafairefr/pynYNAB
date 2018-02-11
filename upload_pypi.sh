#!/bin/bash

if ([ "$TRAVIS_BRANCH" == "master" ] || [ ! -z "$TRAVIS_TAG" ]) &&
      [ "$TRAVIS_PULL_REQUEST" == "false" ]; then

    rm -rf dist

    python setup.py sdist bdist_wheel
    python ynab-api/setup.py sdist bdist_wheel

    twine upload -u $PYPI_USER -p $PYPI_PASSWORD dist/*

else
    echo "Bypassed upload_pypi because not a tagged commit on master"
fi