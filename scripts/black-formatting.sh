#! /bin/bash

set -e

while getopts c flag
do
  case "${flag}" in
    c) RUN_CHECK=true;;
    *) echo "Unknown options...";;
  esac
done

BIN_DIR=bin/
SRC_DIR=pypinball/
TEST_DIR=test/

if [ "$RUN_CHECK" = true ]
then
  echo "Running isort check..."
  isort --check $BIN_DIR $SRC_DIR $TEST_DIR
  echo "Running black formatter check..."
  black --check $BIN_DIR $SRC_DIR $TEST_DIR
else
  echo "Running isort..."
  isort $BIN_DIR $SRC_DIR $TEST_DIR
  echo "Running black formatter..."
  black $BIN_DIR $SRC_DIR $TEST_DIR
fi
