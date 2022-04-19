#! /bin/bash

set -e

echo "Running Python unittests..."

pip install -q .
pytest -q test
