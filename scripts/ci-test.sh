#! /bin/bash

set -e

print_header()
{
  echo -e "\n"
  echo "##########################"
  echo "#" $1 
  echo "##########################"
}

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

print_header "Formatting code"
./scripts/black-formatting.sh -c

print_header "Running Pylint"
./scripts/linting.sh

print_header "Running Unit-tests"
./scripts/run-tests.sh

print_header "Building docs"
./scripts/build-docs.sh

echo "Test suite has PASSED!"
