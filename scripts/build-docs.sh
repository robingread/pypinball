#! /bin/bash

set -e

echo "Building docs..."

pushd docs
make html
popd
