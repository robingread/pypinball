#! /bin/bash

set -e

echo "Running Black formatter check..."

SRC_DIR=pypinball/
TEST_DIR=test/
black --check $SRC_DIR $TEST_DIR