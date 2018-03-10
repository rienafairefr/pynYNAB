#!/bin/bash

set -e

python -m doctr deploy docs

python -m doctr deploy --sync --require-master  --built-docs docs/_build/html "."
python -m doctr deploy --sync --no-require-master  --built-docs docs/_build/html "docs-$TRAVIS_BRANCH"