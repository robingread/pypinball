#! /bin/bash

set -e

source venv/bin/activate

echo "Building docs..."
pip install -q --ignore-installed .
rm -rf docs/build/*
sphinx-apidoc -f -o docs/source/apidoc pypinball/
sphinx-build -v docs/source docs/build/public
