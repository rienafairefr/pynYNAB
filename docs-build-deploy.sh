#!/bin/bash

set -e
cd docs
make html
cd ..

doctr deploy docs

doctr deploy --sync --require-master  --built-docs docs/_build/html "."
doctr deploy --sync --no-require-master  --built-docs docs/_build/html "docs-$TRAVIS_BRANCH"

