#! /bin/bash

set -e

source venv/bin/activate

if [ -d build/ ]; then
  echo "Removing build/ directory"
  rm -rf build/
fi

if [ -d pypinball.egg-info ]; then
  echo "Removing any/all *.egg-info directories"
  rm -rf *.egg-info
fi

pip uninstall -y -q pypinball
./scripts/black-formatting.sh -c
./scripts/run-tests.sh
./scripts/build-docs.sh

echo "Test suite has PASSED!"
