#! /bin/bash

set -e

echo "Running Python unittests & calculating code coverage..."

pip install -q .
coverage run --data-file=coverage/.coverage -m pytest -q test
coverage report -m --data-file=coverage/.coverage
coverage xml -q --data-file=coverage/.coverage -o coverage/coverage.xml