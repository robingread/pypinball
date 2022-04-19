#! /bin/bash

set -e

SRC_DIR=pypinball/
TEST_DIR=test/
black --check $SRC_DIR $TEST_DIR