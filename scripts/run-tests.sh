#! /bin/bash

set -e

echo "Running Python unittests..."

pip install -q .
coverage run -m pytest -q test
