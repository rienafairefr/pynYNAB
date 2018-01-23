#!/bin/bash

set -ev

export NYNAB_LOGGINGLEVEL=error;

tox

if [[ ${TRAVIS_EVENT_TYPE} = "cron" || ${TRAVIS_COMMIT_MESSAGE} = *"[ci-cron]"* ]]; then
    tox -e test_live;
fi

if [ -n "$TRAVIS_TAG" ]; then
    if [ $TAG_NAME != $TRAVIS_TAG ]; then
        echo "This tag is for the wrong version. Got \"$TRAVIS_TAG\" expected \"$TAG_NAME\".";
        exit 1;
    fi
fi