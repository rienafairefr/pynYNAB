#!/bin/bash

set -ev

tox

if [[ ${TRAVIS_EVENT_TYPE} = "cron" || ${TRAVIS_COMMIT_MESSAGE} = *"[ci-cron]"* ]]; then
    tox -c live_tox.ini
fi

if [ -n "$TRAVIS_TAG" ]; then
    if [ $TAG_NAME != $TRAVIS_TAG ]; then
        echo "This tag is for the wrong version. Got \"$TRAVIS_TAG\" expected \"$TAG_NAME\".";
        exit 1;
    fi
fi