#! /bin/bash

set -e
source venv/bin/activate

pylint --verbose --rcfile .pylintrc pypinball || pylint-exit --error-fail $?

if [ $? -ne 0 ]; then
  echo "An error occurred while running pylint." >&2
  exit 1
fi

echo ""
echo "Running MyPy for Type Checking..."
mypy pypinball/ bin/ || true