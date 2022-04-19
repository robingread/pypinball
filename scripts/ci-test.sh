#! /bin/bash

set -e

rm -rf build/
pip uninstall -y pypinball
./scripts/black-formatter.sh
./scripts/run-tests.sh
./scripts/build-docs.sh
