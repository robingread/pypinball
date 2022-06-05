#! /bin/bash

set -e

echo "Building docs..."
sphinx-build docs/source docs/build/public
