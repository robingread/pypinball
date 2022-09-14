#! /bin/bash

set -e

echo "Building docs..."
pip install -q --ignore-installed .
rm -rf docs/build/*
sphinx-apidoc -f -o docs/source/apidoc pypinball/
sphinx-build docs/source docs/build/public
