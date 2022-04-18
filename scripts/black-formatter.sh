#! /bin/bash

set -e

SRC_DIR=pypinball/
TEST_DIR=test/
black --check -v $LINE_LEN $SRC_DIR $TEST_DIR