#!/bin/bash

set -ev

tox

if [[ -v "$TRAVIS" ]]; then
    tox -c live_tox.ini
fi
coveralls

if [ -n "$TRAVIS_TAG" ]; then
    if [ $TAG_NAME != $TRAVIS_TAG ]; then
        echo "This tag is for the wrong version. Got \"$TRAVIS_TAG\" expected \"$TAG_NAME\".";
        exit 1;
    fi
fi