#! /bin/bash

set -e

if [ -d build/ ]; then
  echo "Removing build/ directory"
  rm -rf build/
fi

if [ -d *.egg-info ]; then
  echo "Removing any/all *.egg-info directories"
  rm -rf *.egg-info
fi

pip uninstall -y -q pypinball
./scripts/black-formatter.sh
./scripts/run-tests.sh
./scripts/build-docs.sh

echo "Test suite has PASSED!"
