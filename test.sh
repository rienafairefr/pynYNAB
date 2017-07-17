#!/bin/bash

set -ev

export NYNAB_LOGGINGLEVEL=error;

coverage run -m unittest discover tests;

if [[ ${TRAVIS_EVENT_TYPE} = "cron" || ${TRAVIS_COMMIT_MESSAGE} = *"[ci-cron]"* ]]; then
    python -m unittest discover test_live;
fi