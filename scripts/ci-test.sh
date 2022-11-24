#! /bin/bash

set -e

source venv/bin/activate

python --version

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
./scripts/linting.sh
./scripts/run-tests.sh
./scripts/build-docs.sh

echo "Test suite has PASSED!"
