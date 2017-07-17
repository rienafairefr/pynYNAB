#!/bin/bash

set -ev

if [[ ${TRAVIS_EVENT_TYPE} = "cron" || ${TRAVIS_COMMIT_MESSAGE} = *"[ci-cron]"* ]]; then
    python -m unittest discover test_live;
fi